var startService = function()
{
	$.ajax({
		type: "POST",
		url: "start",
		success: function(data)
		{
			$("#start_button").hide();
			$("#stop_button").fadeIn();
		}
	});
};

var stopService = function()
{
	$.ajax({
		type: "POST",
		url: "stop",
		success: function(data)
		{
			$("#stop_button").hide();
			$("#start_button").fadeIn();
		}
	});
};

$("#start_button").click(startService);
$("#stop_button").click(stopService);