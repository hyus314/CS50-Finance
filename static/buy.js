const shares = document.querySelector('#shares');

shares.addEventListener('input', function() {
    if (shares.value === '' || Number(shares.value) <= 0) {
        shares.style.border = '3px solid red';
        shares.style.boxShadow = '0 0 0 0.2rem rgba(255, 0, 0, 0.25)';
    } else {
        shares.style.border = '';
        shares.style.boxShadow = '';
    }
});
const symbol = document.querySelector('#symbol');

symbol.addEventListener('input', async function() {

    const result = await fetch('/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(symbol.value)
    });

    if (!result.ok || !result) {
        console.log('error')
    }

    const data = await result.json();
    const isValid = JSON.parse(data.isValid);
    
    if (symbol.value.trim() == '') {
        symbol.style.border = '';
        symbol.style.boxShadow = '';
    } else {
        if (isValid) {
            symbol.style.border = '3px solid green';
            symbol.style.boxShadow = '0 0 0 0.2rem rgba(40, 167, 69, 0.25)';
        } else {
            symbol.style.border = '3px solid red';
            symbol.style.boxShadow = '0 0 0 0.2rem rgba(255, 0, 0, 0.25)';
        }
    }
});