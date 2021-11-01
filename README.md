# PYprojectfinder V0.1
根据 projectfinder 使用python3集成的胶水项目。
## 环境安装
- [subfinder]

[subfinder]:https://github.com/projectdiscovery/subfinder
```go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest```
- [httpx]

[httpx]:https://github.com/projectdiscovery/httpx
```go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest```

- [nuclei]

[Nuclei]:https://github.com/projectdiscovery/nuclei
```go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest```
### 使用步骤

- script a 进行项目初始化，包括报告路径创建，数据库创建，从recode.txt读取初始域名列表，后期可以从recode进行增量域名任务更新。
- script b 进行子域名收集整理，调用subfinder，需要自行配置api，数据路径入库，数据保存/report/txt目录。
- script c 进行http/https扫描，调用httpx每次取10条subfinder结果进行，数据路径入库，数据保存/report/json、/report/csv目录。
- script d 进行漏洞扫描，调用nuclei，数据保存/report/txt目录。

```angular2html
python3 a_recode.py
python3 b_subfinder.py
python3 c_httpx.py
python3 d_nuclei.py
```

有任何问题和改进建议，欢迎py :)


