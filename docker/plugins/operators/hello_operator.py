from airflow.models.baseoperator import BaseOperator

class HelloWorldOperator(BaseOperator):
    
    def __init__(self, param1, param2, *args, **kwargs) -> None:
        self.param1 = param1
        self.param2 = param2
        super(HelloWorldOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        print(f'Hello World from Operator: {self.param1} {self.param2}')
