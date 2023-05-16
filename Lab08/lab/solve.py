import angr
import sys

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})

# TODO
main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x40134d

class MyScanf(angr.SimProcedure):
    def run(self, fmt, n):
        simfd = self.state.posix.get_fd(sys.stdin.fileno())
        data, ret_size = simfd.read_data(4)
        self.state.memory.store(n, data)
        return 1

proj.hook_symbol('__isoc99_scanf', MyScanf(),  replace=True)

state = proj.factory.blank_state(addr=main_addr)

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=find_addr, avoid=avoid_addr)
if simgr.found:
    print(simgr.found[0].posix.dumps(sys.stdin.fileno()))

s = simgr.found[0].posix.dumps(sys.stdin.fileno())
ans = []
for i in range(15):
    a = int.from_bytes(s[i * 4 : i * 4 + 4], byteorder='little')
    ans.append(a)
    print(f"x{i}: {a}")

with open('solve_input', 'w') as f:
    for a in ans:
        f.write(f'{a}\n')