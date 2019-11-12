
function validationForm(event) {
	var idList = ["l1", "name", "surname", "email", "number", "town", "pass1", "pass2"];
	for (var i = 0; i < idList.length; i++) {
		if (document.getElementById(idList[i]).value == "" || document.getElementById(idList[i]).value.replace(/\s+/g, '') == "") {
			document.getElementById("send").disabled = true; return false;
		}
		else {document.getElementById("send").disabled = false;
	}
	}
}

function validationPassword(event) {
	var value1 = document.getElementById("pass1").value;
	var value2 = document.getElementById("pass2").value;
	if (value1 != value2 ) {
			document.getElementById("hdn_msg").className = "msg_visible"; return false;
	} else {document.getElementById("hdn_msg").className = "msg_non_visible";}
}

document.getElementById("l1").addEventListener("keyup", validationForm);
document.getElementById("name").addEventListener("keyup", validationForm);
document.getElementById("surname").addEventListener("keyup", validationForm);
document.getElementById("email").addEventListener("keyup", validationForm);
document.getElementById("number").addEventListener("keyup", validationForm);
document.getElementById("dob").addEventListener("keyup", validationForm);
document.getElementById("town").addEventListener("keyup", validationForm);
document.getElementById("pass1").addEventListener("keyup", validationForm);
document.getElementById("pass2").addEventListener("keyup", validationForm);
document.getElementById("send").addEventListener("click", validationPassword);



			