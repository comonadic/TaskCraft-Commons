#!/bin/bash
set -euo pipefail
if kubectl get nodes >/dev/null 2>&1; then exit 0; fi
# Delegate this container's private cgroup v2 subtree before nested containerd.
# Never mount or modify the host cgroup namespace.
if [ -f /sys/fs/cgroup/cgroup.controllers ] && grep -qx '0::/' /proc/1/cgroup; then
  python - <<'CGROUP'
from pathlib import Path
b=Path('/sys/fs/cgroup');(b/'init').mkdir(exist_ok=True)
for pid in (b/'cgroup.procs').read_text().split():
 try:(b/'init/cgroup.procs').write_text(pid)
 except ProcessLookupError:pass
for controller in (b/'cgroup.controllers').read_text().split():(b/'cgroup.subtree_control').write_text('+'+controller)
CGROUP
fi
if ! ip route | grep -q '^default'; then
  ip link add dummy0 type dummy || true
  ip link set dummy0 up
  ip addr add 203.0.113.254/31 dev dummy0 || true
  ip route add default via 203.0.113.255 dev dummy0 metric 1000
fi
mkdir -p /var/lib/rancher/k3s
nohup k3s server --snapshotter=native --write-kubeconfig-mode=644 --kubelet-arg=eviction-hard=memory.available\<100Mi,nodefs.available\<1% --kubelet-arg=fail-swap-on=false --kubelet-arg=cgroups-per-qos=false --kubelet-arg=enforce-node-allocatable= > /tmp/k3s.log 2>&1 &
for i in $(seq 1 180); do if kubectl get nodes -o name 2>/dev/null | grep -q node/; then break; fi; sleep 2; done
kubectl wait --for=condition=Ready node --all --timeout=180s
