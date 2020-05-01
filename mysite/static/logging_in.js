function logginingIn(event) {
	var idList = ["login", "pass"];
	for (var i = 0; i < idList.length; i++) {
		if (document.getElementById(idList[i]).value == "" || document.getElementById(idList[i]).value.replace(/\s+/g, '') == "") {
			document.getElementById("send_form").disabled = true;
			return false;
		}
		else {document.getElementById("send_form").disabled = false;
	}
	}
}


document.getElementById("login").addEventListener("keyup", logginingIn);
document.getElementById("pass").addEventListener("keyup", logginingIn);