#!/bin/sh
set -eu

tmp="${nsjail_cfg}.ppp"
sed '1,/nosuid:true/s/nosuid:true/nosuid:false/' "$nsjail_cfg" > "$tmp"
printf '\n' >> "$tmp"
cat >> "$tmp" <<'EOF'
disable_no_new_privs: true
persona_addr_no_randomize: true
uidmap { inside_id: "0" outside_id: "" count: 1 }
gidmap { inside_id: "0" outside_id: "" count: 1 }
EOF
mv "$tmp" "$nsjail_cfg"
