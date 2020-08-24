let btn = document.getElementById('pv');


function previewToggle(){
	let mesA = 'Preview [show]';
	let mesB = 'Preview [hide]';
	let clsA = 'invisible';
	let clsB = 'visible';
	let tgl = btn.classList.toggle('pv_on');
	let mode = tgl ? clsA : clsB;
	let anti = tgl ? clsB : clsA;
	let mesX = tgl ? mesA : mesB;
	let targets = document.getElementsByClassName(mode);
	btn.innerHTML = mesX;
	while(targets.length){
		targets[0].classList.toggle(anti);
		targets[0].classList.toggle(mode);
	}
}