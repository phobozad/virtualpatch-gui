<!doctype html>
<html>
<head>
<title>View Switch Ports</title>
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
    <li class="breadcrumb-item active" aria-current="page">View Switch Ports</li>
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
<h1>View Switch Ports</h1>
<table class="table">
   <tr>
	<th>Switch</th>
	<th>Port</th>
	<th>Description</th>
	<th>State</th>
	<th>CDP Neighbors</th>
	<th></th>
  </tr>
%  for intName,intDetails in intList.items():
   <tr>
	<td></td>
	<td>{{intName}}</td>
	<td>{{intDetails["intDescription"]}}</td>
	<td></td>
	<td>
%	  if intName in cdpNeighbors:
%		curCdp=cdpNeighbors[intName]
		<a role="button" class="btn btn-outline-info" data-toggle="popover" data-container="body" data-placement="top" tabindex="0" data-trigger="focus" data-html="true" title="CDP Neighbor Details"
data-content="
    <strong>Device Name:</strong> {{curCdp.get('device-name','')}}<br>
    <strong>Platform:</strong> {{curCdp.get('platform-name', '')}}<br>
    <strong>Version:</strong> {{curCdp.get('version', '')}}<br>
    <strong>Port ID:</strong> {{curCdp.get('port-id', '')}}<br>
    <strong>IP Address:</strong> {{curCdp.get('ip-address', '')}}<br>
    <strong>MGMT IP Address:</strong> {{curCdp.get('mgmt-address', '')}}<br>
    <strong>Capabilities:</strong> {{curCdp.get('capability', '')}}<br>
    <strong>Duplex:</strong> {{curCdp.get('duplex', '').split('-')[1]}}<br>
    <strong>Native VLAN:</strong> {{curCdp.get('native-vlan', '')}}<br>
    <strong>PoE Available:</strong> {{curCdp.get('power-available',{}).get('power-available', '')}}<br>
    <strong>PoE Requested:</strong> {{curCdp.get('power-request', {}).get('power-request-level', '')}}<br>
"> {{cdpNeighbors.get(intName,{}).get("device-name","")}}</a>
%	  end
	</td>
	<td><a href="#"><button type="button" class="btn btn-secondary">Edit...</button></a></td>
   </tr>
%  end

</table>
<script src="//code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="//stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<script>
$(function () {
  $('[data-toggle="popover"]').popover()
  $('.popover-dismiss').popover({
    trigger: 'focus'
  })
})
</script>
</div>
</body>
</html>
