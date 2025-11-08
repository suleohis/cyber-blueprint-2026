# Day 3: Loops - Simplate scanning 50 log entries
print("=== FOR LOOP: Scanning 50 log lines ===")
for i in range(1, 51):
    print(f"Prcessing log entry {i}")

print("\n=== WHILE LOOP: Same task ===")
count = 1
while count <= 50:
    print(f"Processing log entry {count}")
    count += 1 #CRITICAL: increment or infinite loop!