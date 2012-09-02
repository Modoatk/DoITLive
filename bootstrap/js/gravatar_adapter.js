var BASE_URL = "http://www.gravatar.com/avatar/";

var getGravatarURL = function(email)
{
	var emailHash;

	emailHash = md5(email);

	return BASE_URL + emailHash;
};

$(document).ready(function() {
	$("#gravatar_sam").attr("src", getGravatarURL('samp@gleap.org'));
	$("#gravatar_ste").attr("src", getGravatarURL('sthoma4@gmail.com'));
})