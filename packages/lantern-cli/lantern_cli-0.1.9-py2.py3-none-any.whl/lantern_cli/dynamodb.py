import boto3
import click
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from lantern_cli.utils.json import json_decimal_to_float, json_float_to_decimal

def delete_method():
    click.echo('''
             * * * * * * * * * * * * * * *
             *                           * 
             *    DynamoDB DELETE     * 
             *                           *
             * * * * * * * * * * * * * * *''')
    click.echo(click.style('''
        ** We will ask for your confirmation before deleting anything!
        ** Dont"t get too crazy cleaning up dynamo XD''', fg='green'))
    click.pause() # waiting for user keypress
    # Asking for amazon profile (application name and stage)
    amazon_profile = None
    ENV_LIST = ['dev', 'test', 'prod']
    application_name = click.prompt(text='Application Name')
    is_stage_valid = False
    while not is_stage_valid:
        stage = click.prompt(text='Environment (dev, test, prod)')
        is_stage_valid = stage in ENV_LIST
    amazon_profile = "{}_{}".format(application_name, stage)
    click.echo("We will use {amazon_profile}, which should be defined in {folder}".format(
        amazon_profile=click.style('['+amazon_profile+']', fg='green'),
        folder=click.style('~/.aws/credentials', fg='green')))
    # Dynamo Table
    dynamodb_table = click.prompt('DynamoDB table name')
    click.echo("We will use {table} dynamo table".format(table=click.style(dynamodb_table, fg='green')))
    primary_keys = click.prompt("Primary key column names (use , if multiple columns)")
    click.echo('\b')
    
    # query parameters
    click.echo("Please as many filter options as you required!")
    filter_options = []
    is_adding_filters = True
    TYPE_LIST = ['N', 'S']
    TYPE_LIST_MAPPING = {'N': float,'S': str}
    OPERATOR_LIST = ['eq', 'ne', 'lt', 'lte', 'gt', 'gte', 'begins_with', 'between']
    while is_adding_filters:
        column_name = click.prompt('Enter Column Name', type=str)
        # getting type
        is_type_valid = False
        while not is_type_valid:
            type = click.prompt('column_name type {} for String or Number'.format(TYPE_LIST), type=str)
            if type not in TYPE_LIST:
                click.echo(click.style("column_name type should be one of {}".format(TYPE_LIST)))
            else:
                is_type_valid = True
        # getting operator
        is_operator_valid = False
        while not is_operator_valid:
            operator = click.prompt("Operator {}".format(OPERATOR_LIST))
            if operator not in OPERATOR_LIST:
                click.echo(click.style("Operator should be one of {}".format(OPERATOR_LIST)))
            else:
                is_operator_valid = True
        # getting value 1
        value1 = click.prompt("Value: ", type=TYPE_LIST_MAPPING[type])
        # getting value 2 (if required)
        value2 = None
        if type == 'between':
            value1 = click.prompt("Value 2: ", type=TYPE_LIST_MAPPING[type])
        click.echo(" ** New filter confirmation (before adding to filter list)")
        click.echo(
            "New Filter " +
            click.style("%s %s %s" % (column_name, operator, value1), fg="green") if not value2 else click.style("%s %s (%s, %s)" % (column_name, operator, value1, value2), fg="green"))
        if click.confirm("Do you want add this filter?"):
            filter_options.append({"column_name": column_name, "operator": operator, "type": type, "value1": value1, "value2": value2 })
            click.echo(click.style("Filter added to your list of filters", fg="green"))
        else:
            click.echo(click.style('Filter ignored', fg="red"))
        if not click.confirm("Would you like to add an additional filter?"):
            is_adding_filters = False
    
    # Presenting Query to user
    click.echo(
        "Fetching data from table: " +
        click.style(dynamodb_table, fg="green") +
        " with following filters \n" +
        "\n".join([
            "\t - " +
            "%s %s %s" % (x['column_name'], x['operator'], x['value1']) if not x["value2"] else "%s %s (%s, %s)" % (x['column_name'], x['operator'], x['value1'], x['value2'])
            + "\n"
            for x in filter_options
        ])
    )

    # getting filter expression
    if not len(filter_options):
        click.echo(click.style("At least 1 filter is required", fg="red"))
        return True
    filter_expression = None
    # getting filter expression
    for filter in filter_options:
        column_name = filter['column_name']
        operator = filter['operator']
        type = filter['type']
        value1 = filter['value1']
        value2 = filter['value2']
        if type == 'N' and value1 is not None:
            value1 = Decimal(value1)
        if type == 'N' and value2 is not None:
            value = Decimal(value)
        if operator == 'eq':
            new_fe = Key(column_name).eq(value1)
        if operator == 'ne':
            new_fe = Key(column_name).ne(value1)
        if operator == 'lt':
            new_fe = Key(column_name).lt(value1)
        if operator == 'lte':
            new_fe = Key(column_name).lte(value1)
        if operator == 'gt':
            new_fe = Key(column_name).gt(value1)
        if operator == 'gte':
            new_fe = Key(column_name).gte(value1)
        if operator == 'begins_with':
            new_fe = Key(column_name).begins_with(value1)
        if operator == 'between':
            if not value2:
                raise Exception("value2 not defined")
            new_fe = Key(column_name).between(value1, value2)
        filter_expression = new_fe if not filter_expression else filter_expression & new_fe
    
    # getting data from dynamodb
    click.echo(click.style('Pulling data from DynamoDB, just a sec...'))
    session = boto3.Session(profile_name=amazon_profile)
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table)
    response = table.scan(FilterExpression=filter_expression)
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(FilterExpression=filter_expression, ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    # rendering data
    data = json_decimal_to_float(data)
    data_cont = len(data)
    click.secho("%s rows pulled from dynamo" % data_cont, blink=True, bold=True)
    if not data_cont:
        click.secho("No data found with those params", blink=True, bold=True)
    click.pause()
    in_preview_mode = True
    while in_preview_mode:
        click.echo_via_pager("\n".join(["{} of {}: {}".format(idx, data_cont, row) for idx, row in enumerate(data)]), color=True)
        if not click.confirm("Whould you like to preview data again?"):
            in_preview_mode = False
    # Confirmation for delete
    click.echo("\n**\n")
    click.echo(click.style("WARNING! In this section you will confirm you wanna delete {} rows you just saw in preview mode".format(data_cont), fg="red"))
    is_confirming = True
    should_delete = False
    while is_confirming:
        confirmation_txt = click.prompt(click.style("please type DELETE_ALL for deleting all selected rows", fg="red"))
        if confirmation_txt == 'DELETE_ALL':
            should_delete = True
            is_confirming = False
        else:
            if click.confirm("You missed that one XD, whould you like to try it again?"):
                is_confirming = True
            else:
                is_confirming = False
    if not should_delete:
        click.echo(click.style("No action taken. No data deleted. and we just missed 3min of our lifes", fg="red"))
        return True #finishing program
    
    # deleting data
    with click.progressbar(data) as data_bar:
        with table.batch_writer() as batch:
            for row in data_bar:
                pk = {}
                for key in primary_keys.split(','):
                    key = key.replace(' ', '')
                    pk[key] = row[key]
                pk = json_float_to_decimal(pk)
                batch.delete_item(Key=pk)
    
    click.echo(click.style("You just deleted {} rows in {} table".format(data_cont, dynamodb_table)))

