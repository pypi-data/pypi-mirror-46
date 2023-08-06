# Hippo2client

## Installation

Simple install this module via pip (pip for Python 2 is also supported)

```
pip3 install --user hippo2client
```


## Usage

```
import hippo2client

e = hippo2client.MajorEntity('v1.2.4')

meta = hippo2client.MetaTest(hippo2client.MetaTest.PASSED)
e.minor_add_meta('0001', meta)

e.add_markdown('001', '[test-001](0001/)')
e.add_reference('0001', '002.md', 'link to 0001')
e.minor_add_markdown('0001', '01.md', 'test **passed**')
path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
e.minor_add_file('0001', "graph.png", path_to_image)
e.minor_add_markdown('0001', '02.md', '![graph](graph.png)')

URL = "http://localhost:8080/"
TIMEOUT = 10
a = hippo2client.Agent(url=URL, timeout=TIMEOUT)
a.add(e)
a.upload()
```

