# endpoint-hunter-1.1

Installation

Clone the repository:
```bash
git clone https://github.com/FabioBarbosaSantos/endpoint-hunter-1.1.git
cd endpoint-hunter-1.1
pip install -r requirements.txt
playwright install
```
or
```bash
pip install --break-system-packages -r requirements.txt
playwright install
```

Run the tool:
```bash
python3 main.py -u https://example.com
```
Specify number of threads:
```bash
python3 main.py -u https://example.com -t 30
```
-t:
```
  5 → shy
  
  10 → normal
  
  20 → fast
  
  50+ → agresiv
```

Features:

```
  Extracts internal JavaScript files from target HTML
  
  Parses JavaScript files to discover endpoints
  
  Normalizes relative paths to absolute URLs
  
  Filters external domains automatically
  
  Multithreaded endpoint validation
  
  Displays HTTP status code next to each valid endpoint
```
