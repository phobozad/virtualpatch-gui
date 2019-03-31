<!doctype html>
<html>
<head>
<title>Add New Patch</title>
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
    <li class="breadcrumb-item"><a href="/">Patch Panel</a></li>
    <li class="breadcrumb-item active" aria-current="page">Add New Patch</li>
  </ol>
</nav>
% if statusMessage:
	<div class="alert alert-success alert-dismissible fade show" role="alert">
	{{statusMessage}}
	<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
	</div>
% end
% if errorMessage:
	<div class="alert alert-danger" role="alert">
	{{errorMessage}}
	<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
	</div>
% end

<div class="container">
<h1>Add New Patch</h1>
<form action="/xc/add" method="post">
<table class="table">
<tr> <th>Patch ID</th> <th>A-Side</th> <th>Z-Side</th> </tr>
<tr>
	<td>
		<input name="xcName" id="xcName" type="text" class="form-control" placeholder="Patch ID">
	</td>
	<td>
		<select id="a-side" name="a-side" class="form-control">
%		for xcInt,xcIntDetails in xcIntOptions.items():
		   <option value="{{xcInt}}">{{xcInt + " - " + xcIntDetails["intDescription"]}}</option>
%		end
		</select>
	</td>
	<td>
		<select id="z-side" name="z-side" class="form-control">
%		for xcInt,xcIntDetails in xcIntOptions.items():
		   <option value="{{xcInt}}">{{xcInt + " - " + xcIntDetails["intDescription"]}}</option>
%		end
		</select>
	</td>
</tr>
</table>
<input type="Submit" value="Add" class="btn btn-primary"> <a href="/"><button type="button" class="btn btn-secondary">Cancel</button></a>
</form>

<script src="//code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="//stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</div>
</body>
</html>
