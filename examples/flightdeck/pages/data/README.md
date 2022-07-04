
* [json-generator.com](https://json-generator.com/#)
* [json-to-csv.com](https://www.convertcsv.com/json-to-csv.htm)

*subscriptions.csv*
```
[
  '{{repeat(500, 500)}}',
  {
    ID: '{{integer(45000, 46000)}}',
    Bill_For: '{{random("Platinum Subscription Plan", "Gold Subscription Plan", "Flexible Subscription Plan")}}',
    Issue_Date: '{{date(new Date(2020, 0, 1), new Date(), "dd MMM YYYY")}}',
    Due_Date: '{{date(new Date(2021, 0, 1), new Date(), "dd MMM YYYY")}}',
    Total: '{{floating(200, 1000, 2, "$0,0.00")}}',
    Status: '{{random("Paid", "Due", "Cancelled")}}',
    Action: '-'

  }
]
```