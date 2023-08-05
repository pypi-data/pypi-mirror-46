from objectbox.model.entity import _Entity
from objectbox.objectbox import ObjectBox
from objectbox.c import *


class Box:
    def __init__(self, ob: ObjectBox, entity: _Entity):
        if not isinstance(entity, _Entity):
            raise Exception("Given type is not an Entity")

        self._ob = ob
        self._entity = entity
        self._c_box = obx_box(ob._c_store, entity.id)

    def is_empty(self) -> bool:
        is_empty = ctypes.c_bool()
        obx_box_is_empty(self._c_box, ctypes.byref(is_empty))
        return bool(is_empty.value)

    def count(self, limit: int = 0) -> int:
        count = ctypes.c_uint64()
        obx_box_count(self._c_box, limit, ctypes.byref(count))
        return int(count.value)

    def put(self, *objects):
        """Puts an object (or a list of objects) and returns its ID (or nothing for a list objects)"""

        if len(objects) != 1:
            self._put_many(objects)
        elif isinstance(objects[0], list):
            self._put_many(objects[0])
        else:
            return self._put_one(objects[0])

    def _put_one(self, obj) -> int:
        id = object_id = self._entity.get_object_id(obj)

        if not id:
            id = obx_box_id_for_put(self._c_box, 0)

        data = self._entity.marshal(obj, id)
        obx_box_put(self._c_box, id, bytes(data), len(data), OBXPutMode_PUT)

        if id != object_id:
            self._entity.set_object_id(obj, id)

        return id

    def _put_many(self, objects) -> None:
        # retrieve IDs from the objects (to distinguish new objects and updates)
        new = {}
        ids = {}
        for k in range(len(objects)):
            id = self._entity.get_object_id(objects[k])
            if not id:
                new[k] = 0
            ids[k] = id

        # acquire IDs for the new objects and set them
        if len(new) > 0:
            c_next_id = obx_id()
            obx_box_ids_for_put(self._c_box, len(new), ctypes.byref(c_next_id))
            next_id = c_next_id.value
            for k in new.keys():
                ids[k] = next_id
                next_id += 1

        # allocate a C bytes array structure where we will push the object data
        # OBX_bytes_array with .count = len(objects)
        c_bytes_array_p = obx_bytes_array_create(len(objects))

        try:
            # we need to keep the data around until put_many is executed because obx_bytes_array_set doesn't do a copy
            data = {}
            for k in range(len(objects)):
                data[k] = bytes(self._entity.marshal(objects[k], ids[k]))
                key = ctypes.c_size_t(k)

                # OBX_bytes_array.data[k] = data
                obx_bytes_array_set(c_bytes_array_p, key, data[k], len(data[k]))

            c_ids = (obx_id * len(ids))(*ids.values())
            obx_box_put_many(self._c_box, c_bytes_array_p, c_ids, OBXPutMode_PUT)

        finally:
            obx_bytes_array_free(c_bytes_array_p)

        # assign new IDs on the object
        for k in new.keys():
            self._entity.set_object_id(objects[k], ids[k])

    def get(self, id: int):
        c_data = ctypes.c_void_p()
        c_size = ctypes.c_size_t()
        obx_box_get(self._c_box, id, ctypes.byref(c_data), ctypes.byref(c_size))

        data = c_voidp_as_bytes(c_data, c_size.value)
        return self._entity.unmarshal(data)

    def get_all(self) -> list:
        # OBX_bytes_array*
        c_bytes_array_p = obx_box_get_all(self._c_box)

        try:
            # OBX_bytes_array
            c_bytes_array = c_bytes_array_p.contents

            result = list()
            for i in range(c_bytes_array.count):
                # OBX_bytes
                c_bytes = c_bytes_array.data[i]
                data = c_voidp_as_bytes(c_bytes.data, c_bytes.size)
                result.append(self._entity.unmarshal(data))

            return result
        finally:
            obx_bytes_array_free(c_bytes_array_p)

    def remove(self, id_or_object):
        if isinstance(id_or_object, self._entity.cls):
            id = self._entity.get_object_id(id_or_object)
        else:
            id = id_or_object
        obx_box_remove(self._c_box, id)

    def remove_all(self) -> int:
        count = ctypes.c_uint64()
        obx_box_remove_all(self._c_box, ctypes.byref(count))
        return int(count.value)
