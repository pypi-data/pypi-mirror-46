# fmqlreports

Reports from FMQL Data building on fmqlutils

## Installing (until pip)

> python setup.py install

## Generating Reports

Simple report by report by invoking _main_ of each report. For example for the basics' report, _webReportDataTypes_ ...

> python -m fmqlreports.basics.webReportDataTypes {SN}

## Serving Report Site

Steps to create:

> cp -r ReportSiteTemplate /data/vista/{SN}/ReportSite
> cd /data/vista/{SN}/ReportSite
> vi _config.yml (update title and port)
> jekyll serve

Note: blank index.md to start - need to generate in
