<!doctype html>
<html>
<head>
<title>Edit Patch - {{xcName}}</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<style>
.alert:empty {
 display: none;
}
</style>
</head>
<body>
<nav class="navbar navbar-dark bg-dark">
  <span class="navbar-brand mb-0 h1">Virtual Patch Panel</span>
</nav>
<div class="alert alert-success" role="alert">{{statusMessage}}</div>
<div id="error" class="alert alert-danger" role="alert">{{errorMessage}}</div>
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="/">Patch Panel</a></li>
    <li class="breadcrumb-item active" aria-current="page">Edit Patch</li>
  </ol>
</nav>
<div class="container">
<h1>Edit Patch - {{xcName}}</h1>
<form action="/xcedit/{{xcName}}" method="post">
<table class="table">
<tr> <th>Patch ID</th> <th>A-Side</th> <th>Z-Side</th> </tr>
<tr>
	<td>{{xcName}}</td>
	<td>
		<select id="a-side" name="a-side" class="form-control">
% for xcInt in xcIntOptions:
		<option value="{{xcInt["intName"]}}">{{xcInt["intName"] + " - " + xcInt["intDescription"]}}</option>
% end
		</select>
	</td>
	<td>
		<select id="z-side" name="z-side" class="form-control">
% for xcInt in xcIntOptions:
		<option value="{{xcInt["intName"]}}">{{xcInt["intName"] + " - " + xcInt["intDescription"]}}</option>
% end
		</select>
	</td>
</tr>
</table>
<br><br>
<input type="Submit" value="Save" class="btn btn-primary"> <a href="/"><button type="button" class="btn btn-secondary">Cancel</button></a>
</form>
<script>
	document.getElementById("a-side").value="{{curASide}}"
	document.getElementById("z-side").value="{{curZSide}}"
</script>
<script src="//code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="//stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</div>
</body>
</html>
