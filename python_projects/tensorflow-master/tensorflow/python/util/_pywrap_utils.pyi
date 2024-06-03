# Copyright 2023 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

def AssertSameStructure(arg0: object, arg1: object, arg2: bool, arg3: bool) -> bool: ...
def AssertSameStructureForData(arg0: object, arg1: object, arg2: bool) -> bool: ...
def Flatten(arg0: object, arg1: bool) -> object: ...
def FlattenForData(arg0: object) -> object: ...
def IsAttrs(arg0: object) -> bool: ...
def IsBF16SupportedByOneDNNOnThisCPU() -> bool: ...
def IsCompositeTensor(arg0: object) -> bool: ...
def IsMapping(arg0: object) -> bool: ...
def IsMappingView(arg0: object) -> bool: ...
def IsMutableMapping(arg0: object) -> bool: ...
def IsNamedtuple(arg0: object, arg1: bool) -> object: ...
def IsNested(arg0: object) -> bool: ...
def IsNestedForData(arg0: object) -> bool: ...
def IsNestedOrComposite(arg0: object) -> bool: ...
def IsResourceVariable(arg0: object) -> bool: ...
def IsTensor(arg0: object) -> bool: ...
def IsTypeSpec(arg0: object) -> bool: ...
def IsVariable(arg0: object) -> bool: ...
def RegisterPyObject(arg0: object, arg1: object) -> object: ...
def RegisterType(arg0: object, arg1: object) -> object: ...
def SameNamedtuples(arg0: object, arg1: object) -> object: ...
