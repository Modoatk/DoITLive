var toggleService = function()
{
	$.ajax({
		type: "POST",
		url: "start",
	});
};

$("#button").click(toggleService)
