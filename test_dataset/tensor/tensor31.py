def testRepr(self):
    self.skipTest("b/142725777")
    for enum, name in dtypes._TYPE_TO_STRING.items():
      if enum > 100:
        continue
      dtype = dtypes.DType(enum)
      self.assertEqual(repr(dtype), "tf." + name)
      import tensorflow as tf
      dtype2 = eval(repr(dtype))
      self.assertEqual(type(dtype2), dtypes.DType)
      self.assertEqual(dtype, dtype2)

