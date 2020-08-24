function setClipboard(e){
	let input = document.createElement('input');
	input.setAttribute('id', 'copyinput');
	document.body.appendChild(input);
	input.value = this.value;
	input.select();
	document.execCommand('copy');
	document.execCommand('copy');
	document.body.removeChild(input);
}


function SetListenerCopyButton(){
	Array.from(document.getElementsByClassName('v_directory')).forEach((row, index)=>{
		row.getElementsByClassName('copy')[0].addEventListener(
			'click', {
				value: String(row.getElementsByClassName('view')[0].getAttribute('value')),
				handleEvent: setClipboard
			}
		);
	})
}
SetListenerCopyButton();

