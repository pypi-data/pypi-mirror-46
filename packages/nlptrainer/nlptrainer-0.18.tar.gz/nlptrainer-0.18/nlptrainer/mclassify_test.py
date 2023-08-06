import mclassifier as mc
import json

tp={0: 1, 1: 1}
fp={0: 1, 1: 1}
fn={0: 1, 1: 1}
precision={0: 0.5, 1: 0.5}
recall = {0: 0.5, 1: 0.5 }
map={0: 'class A', 1: 'class B'}

result = mc.parseResult(tp, fp, fn, precision, recall, map)
print(json.dumps(result))
