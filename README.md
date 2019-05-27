![logo](https://github.com/gruunday/MasterDoc/blob/master/docs/MasterDoc/images/MasterDocBannerSmall.png?raw=true)

# MasterDoc

This is a tool to consolidate all the docs for a github organisation into a master repository that can then be deployed.

This means that the docs for all services will be in the repository they beylong to and tracked with the rest of the source code.


### Dependencies

[pygithub](https://pygithub.readthedocs.io/en/latest/index.html)


```
pip install pygithub
```

### Install

```
git clone https://github.com/gruunday/MasterDoc.git
python3 src/collector.py
docker-compose up -d
```

### Testing 

```
python3 src/collector.py && mkdocs serve -a 0.0.0.0:8000
```
