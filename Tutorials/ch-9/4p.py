word = "donkey"
with open("donkey_paragraphs.txt") as f:
    content = f.read()

newcontent = content.replace("donkey", "######")

with open("donkey_paragraphs.txt", "w") as w:
    w.write(newcontent)