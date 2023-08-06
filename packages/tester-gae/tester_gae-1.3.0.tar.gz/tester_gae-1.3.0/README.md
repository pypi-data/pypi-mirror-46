# Class for autotests GoogleAppEngine python apps
[![Python 2.7](https://img.shields.io/travis/vb64/test.helper.gae.svg?label=Python%202.7&style=plastic)](https://travis-ci.org/vb64/test.helper.gae)
[![Code Climate](https://img.shields.io/codeclimate/maintainability-percentage/vb64/test.helper.gae.svg?label=Code%20Climate&style=plastic)](https://codeclimate.com/github/vb64/test.helper.gae)
[![Coverage Status](https://coveralls.io/repos/github/vb64/test.helper.gae/badge.svg?branch=master)](https://coveralls.io/github/vb64/test.helper.gae?branch=master)

## Install
```
$ pip install tester_gae
```

## Usage in tests

```python

from tester_gae import TestGae

class TestGaeApp(TestGae):
    """
    test GAE app
    """
    def setUp(self):
        TestGae.setUp(self, "path/to/you/gae/app/dir")  # where app.yaml located

    def test_check_db_tables(self):
        """
        check db table items count
        """
        from main import TestTable

        self.check_db_tables([
          (TestTable, 0),
        ])

        item = TestTable()
        item.put()

        self.check_db_tables([
          (TestTable, 1),
        ])

    def test_queue(self):
        """
        check for number of tasks in queue
        """
        from google.appengine.api.taskqueue import Queue, Task

        self.queue = Queue('default')
        self.queue.add(Task('xxx', url='/'))

        self.assert_tasks_num(1)
        tasks = self.gae_tasks(queue_name='default', flush_queue=False)

        self.assertEqual(len(tasks), 1)
        self.assert_tasks_num(1)

        tasks = self.gae_tasks(queue_name='default', flush_queue=True)
        self.assertEqual(len(tasks), 1)
        self.assert_tasks_num(0)

```
