<html>
<head><title>Edit Patch ID {{xcName}}</title></head>
<body>
<h1>Edit Patch ID {{xcName}}</h1>
<h3>{{statusMessage}}</h3>
<form action="/edit/{{xcName}}" method="post">
<table border=1>
<tr> <th>Patch ID</th> <th>A-Side</th> <th>Z-Side</th> </tr>
<tr>
	<td>{{xcName}}</td>
	<td>
		<select id="a-side" name="a-side">
% for xcInt in xcIntOptions:
		<option value="{{xcInt["intName"]}}">{{xcInt["intName"] + " - " + xcInt["intDescription"]}}</option>
% end
		</select>
	</td>
	<td>
		<select id="z-side" name="z-side">
% for xcInt in xcIntOptions:
		<option value="{{xcInt["intName"]}}">{{xcInt["intName"] + " - " + xcInt["intDescription"]}}</option>
% end
		</select>
	</td>
</tr>
</table>
<br><br>
<input type="Submit" value="Save"> <a href="/"><button type="button">Cancel</button></a>
</form>
<script>
	document.getElementById("a-side").value="{{curASide}}"
	document.getElementById("z-side").value="{{curZSide}}"
</script>
</body>
</html>
