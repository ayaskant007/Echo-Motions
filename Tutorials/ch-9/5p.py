words = ["midnight", "Maple Street", "Detective Martinez"]
with open("censor.txt") as f:
    content = f.read()
for i in words:
    content = content.replace(i, "------")

with open("censor.txt", "w") as w:
    w.write(content)
