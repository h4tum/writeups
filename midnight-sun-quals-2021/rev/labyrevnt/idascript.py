import ida_funcs
import idautils
import ida_allins
import bisect


##################################################################################################
# https://reverseengineering.stackexchange.com/questions/1646/how-to-map-an-arbitrary-address-to-its-corresponding-basic-block-in-ida
# Wrapper to operate on sorted basic blocks.
class BBWrapper(object):
  def __init__(self, ea, bb):
    self.ea_ = ea
    self.bb_ = bb

  def get_bb(self):
    return self.bb_

  def __lt__(self, other):
    return self.ea_ < other.ea_

# Creates a basic block cache for all basic blocks in the given function.
class BBCache(object):
  def __init__(self, f):
    self.bb_cache_ = []
    for bb in idaapi.FlowChart(f):
      self.bb_cache_.append(BBWrapper(bb.start_ea, bb))
    self.bb_cache_ = sorted(self.bb_cache_)

  def find_block(self, ea):
    i = bisect.bisect_right(self.bb_cache_, BBWrapper(ea, None))
    if i:
      return self.bb_cache_[i-1].get_bb()
    else:
      return None

caches = {}
def get_bbcache(fea):
    if fea not in caches:
        caches[fea] = BBCache(ida_funcs.get_func(fea))
    return caches[fea]

def get_basic_block(ea):
    fea = ida_funcs.get_func(ea).start_ea
    return get_bbcache(fea).find_block(ea)

###############################################################################################











def GetWalkFunction(ea):
    f = ida_funcs.get_func(ea)
    fn = ida_funcs.get_func_name(f.start_ea)
    if 'walk' in fn:
        return (f.start_ea, fn)

    f = ida_funcs.get_func(f.start_ea-1)
    fn = ida_funcs.get_func_name(f.start_ea)

    if 'walk' in fn:
        return (f.start_ea, fn)
    return (None, None)

def GetFunctionByName(name):
    for f in Functions():
        if ida_funcs.get_func_name(f) == name:
            return GetWalkFunction(f)
    return None


def GetPredecessors(func_ea):
    l = []
    for ref in idautils.XrefsTo(func_ea):
        f, fn = GetWalkFunction(ref.frm)
        if f is None:
            continue
        l.append((f, fn))
    return l



def GetSwitchIdx(jmptable, target):
    for i in range(256):
        jmptable_idx = jmptable + i * 4
        addr = ida_bytes.get_dword(jmptable_idx)
        jmpaddr = (jmptable + addr) % (1 << 32)
        #print("Checking jmpaddr ({:x}) == target ({:x})".format(jmpaddr, target))
        if jmpaddr == target:
            return i
    return None


def GetJumpTableAndOffset(walkfunc_ea):
    found_offset = False
    found_jmptable = False
    off = None
    jmptable = None

    f = ida_funcs.get_func(walkfunc_ea)

    for ea in Heads(f.start_ea, f.end_ea):
        if found_offset and found_jmptable:
            break
        insn = idaapi.insn_t()
        length = idaapi.decode_insn(insn, ea)
        if insn.itype == ida_allins.NN_sub:
            off = insn.ops[1].value
            found_offset = True
        # Look for jmp rax and then look back at last lea
        elif insn.itype == ida_allins.NN_jmp and insn.ops[0].reg == idautils.procregs.eax.reg:
            lea_ea = ea
            while lea_ea > f.start_ea:
                lea_ea = ida_bytes.prev_head(lea_ea, 0)
                lea_insn = idaapi.insn_t()
                lea_length = idaapi.decode_insn(lea_insn, lea_ea)
                if lea_insn.itype != ida_allins.NN_lea:
                    continue

                # hack
                jmp_off = ida_bytes.get_dword(lea_ea+3)
                jmptable = lea_ea + jmp_off + 7
                #jmptable = lea_insn.ops[1].value
                found_jmptable = True
                break
    print("ea: {:x}, jmptable: {:x}, off: {:x}".format(walkfunc_ea, jmptable, off))
    return jmptable, off


def GetSwitchCondition(bb_ea):
    jmptable, off = GetJumpTableAndOffset(bb_ea)
    switchidx = GetSwitchIdx(jmptable, bb_ea)

    assert jmptable is not None and off is not None and switchidx is not None

    return chr(off + switchidx)



def GetCharacterCondition(call_ea):
    bb = get_basic_block(call_ea)

    prev_refs = list(idautils.XrefsTo(bb.start_ea))
    if len(prev_refs) != 1:
        return GetSwitchCondition(bb.start_ea)
    assert(len(prev_refs) == 1)
    refea = prev_refs[0].frm

    prev_inst = ida_bytes.prev_head(refea, 0)

    ov = get_operand_value(prev_inst, 1)
    return chr(ov)

# Do DFS
visited = set()

end_ea, end_fn = GetFunctionByName('walk_end')

stack = []

def visit_func(fea, fname):
    stack.append((fea, fname))
    visited.add(fea)
    if fname == 'walk_start':
        return True
    for pfea, pfname in GetPredecessors(fea):
        if pfea in visited:
            continue
        if visit_func(pfea, pfname):
            return True
    stack.pop()


def BuildPassword(stack):
    pw = ""
    for (fea, fname), (pfea, pfname) in zip(stack[:-1], stack[1:]):
        for ref in idautils.XrefsTo(fea):
            f, fn = GetWalkFunction(ref.frm)
            if (fn == pfname):
                pw += GetCharacterCondition(ref.frm)
                break
    return pw[::-1]


visit_func(end_ea, end_fn)

print(stack)
print(BuildPassword(stack))


