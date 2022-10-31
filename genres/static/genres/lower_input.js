document.querySelector('form').addEventListener('submit', e=>{
	e.preventDefault();
	const input = document.querySelector('#id_genre_name');
	input.value = input.value.toLowerCase();
	e.target.submit();
})