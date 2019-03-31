<html>
<head><title>Virtual Patch Panel</title></head>
<body>
<h1>Virtual Patch Panel</h1>
<table border=1>
<tr> <th>Patch ID</th> <th>A-Side</th> <th>Z-Side</th> </tr>
% for xcName,xcInts in localXcList.items():
    <tr> <td>{{xcName}}</td> <td>{{xcInts["a-side"]}}</td> <td>{{xcInts["z-side"]}}</td> <td><a href="/edit/{{xcName}}"><button type="button">Edit...</button></a></td></tr>
% end
</table>
</body>
</html>
