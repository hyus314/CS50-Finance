 // empty url after redirection
 let baseUrl = window.location.origin + window.location.pathname;

 history.pushState({}, document.title, baseUrl);

 const alerts = document.querySelectorAll('.alert');
 for (const alert of alerts) {
     setTimeout(function () {
         alert.style.display = "none";
     }, 8000);
 }

// stocks input js code
let globalStocks = [];
const stocksMenu = document.querySelector('#stocks');

window.addEventListener('load', async function () {
    const request = await fetch('/stocks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const data = await request.json();
    const stocks = Array.from(data.data);
    globalStocks = JSON.parse(JSON.stringify(stocks));
    // console.log(stocks);


    for (let i = 0; i < stocks.length; i++) {
        option = document.createElement('option');
        option.value = stocks[i].name;
        option.textContent = stocks[i].name;
        if (i === 0) {
            option.classList.add('selected');
            let actualStock = globalStocks.find(s => s.name === option.value);
            calculate(actualStock);
        }
        stocksMenu.appendChild(option);
    }

    findStock();

});

stocksMenu.addEventListener('change', function() {
    const options = this.options;
    for (let i = 0; i < options.length; i++) {
        if (options[i].selected) {
            // Remove the 'selected' class from all options
            options[i].classList.add('selected');
            } else {
                options[i].classList.remove('selected');
            }

        }
        let selectedStock = document.querySelector('.selected').value;
        let actualStock = globalStocks.find(s => s.name === selectedStock);
        calculate(actualStock);
    });

const shares = document.querySelector('#shares');

stocksMenu.addEventListener('change', findStock);

function findStock() {
    let selectedStock = document.querySelector('.selected').value;
    let actualStock = globalStocks.find(s => s.name === selectedStock);
    populateSharesInput(actualStock);
}

function populateSharesInput(stock) {
    const sharesToPopulate = document.querySelector('#shares');
    shares.value = stock.shares;
}

shares.addEventListener('input', async function () {
    // Remove non-numeric characters and decimals from the input
    this.value = this.value.replace(/[^0-9]/g, '');
    let selectedStock = document.querySelector('.selected').value;
    let actualStock = globalStocks.find(s => s.name === selectedStock);

    if (this.value > actualStock.shares) {
        this.value = actualStock.shares;
    } else if (this.value < 0) {
        this.value = 1;
    }
    await calculate(actualStock);
});

async function calculate(stock) {

    const result = await fetch('/quotejson', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(stock.name)
    });

    const data = await result.json();
    const liveStock = data.stock;
    const shares = document.querySelector('#shares').value;
    const totalSum = liveStock.price * shares;

    const calculationsDiv = document.querySelector('.calculations-div');
    const array = Array.from(calculationsDiv.children);
    array[1].innerHTML = `The price per share of <p class="lead symbol">${liveStock.symbol}</p> currently is <p class="lead share-price">$${liveStock.price}</p>`;
    array[2].innerHTML = `Total: <p class="lead total-sum">$${totalSum.toFixed(2)}</p>`
}

