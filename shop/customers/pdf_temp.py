temp_pdf='''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <style>
        
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">

    <title>invoice</title>
  </head>
  <body>
    

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-12">
                Invoice: {{orders.invoice}}
                <br>
                Status: {{orders.status}}
                <br>
                Customer Name: {{customer.fname}} {{customer.lname}}
                <br>
                Customer Email: {{customer.email}}
                <br>
                <br>
                <table class="table table-sm">
                    <thead>
                        <th>Sr</th>
                        <th>Name</th>
                        <th>Color(s)</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Subtotal</th>
                    </thead>
                    <tbody>
                        <tr>
                        {% for key, prod in orders.orders.items() %}
                        <td>{{loop.index}}</td>
                        
                            <td> {{prod.name}} </td>
                            <td>{% for color,qty in prod.colors.items() %}
                                {% if qty == 1%}
                                    {{color}},
                                {%else%}
                                    {{qty}} {{color}},
                                {%endif%}
                                {%endfor%}
                            </td>
                            <td>{{prod.price}} </td>
                            <td>{{prod.quantity}} </td>
                            {%set subtotal = prod.quantity * prod.price| float %}
                        <td>${{"%.2f"|format(subtotal|round(1,'floor'))}} </td>
                        </tr>
                        {% endfor%}
                    </tbody>
                </table>
                <table class="table table-sm">
                    <tr>
                        
                        <td width="35%"></td>
                        <td><h5>Tax: ${{tax}}</h5></td>
                        <td><h5>Grand Total: ${{grandtotal}} </h5></td>

                    </tr>
                </table>
            </div>
        </div>
    </div>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>

    
  </body>
</html>
'''