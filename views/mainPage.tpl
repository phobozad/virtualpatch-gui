<!doctype html>
<html>
<head>
<title>Virtual Patch Panel</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
<nav class="navbar navbar-dark bg-dark">
  <span class="navbar-brand mb-0 h1">Virtual Patch Panel</span>
</nav>
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item active" aria-current="page">Patch Panel</li>
  </ol>
</nav>
<div class="container">
<h1>Patch Panel</h1>
<table class="table">
<tr> <th>Patch ID</th> <th>A-Side</th> <th>Z-Side</th> <th></th></tr>
% for xcName,xcInts in localXcList.items():
    <tr> <td>{{xcName}}</td> <td>{{xcInts["a-side"]}}</td> <td>{{xcInts["z-side"]}}</td> <td><a href="/xcedit/{{xcName}}"><button type="button" class="btn btn-secondary">Edit...</button></a>  <button type="button" class="btn btn-danger">Delete</button></td></tr>
% end
</table>
<button type="button" class="btn btn-primary">Add Patch...</button>
<a href="/ports"><button type="button" class="btn btn-secondary">View Switch Ports</button></a>
<br>
<script src="//code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="//stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</div>
</body>
</html>
