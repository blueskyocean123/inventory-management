let arr = [];
let cart = [];
let showCart = [];
const input = document.getElementById("value");
const optionsVal = document.getElementById("list");
const dropdown = document.getElementById("dropdown");
const productValue = document.getElementById("productValue");
const customerPhone = document.getElementById("customerPhone");
const customerName = document.getElementById("customerName");
const productPrice = document.getElementById("productPrice");
const productQuantity = document.getElementById("productQuantity");
const loading = document.getElementById("loading");
const message = document.getElementById("message");
const sellSubmit = document.getElementById("sellSubmit");

let customerId = null;

const csrf = document.getElementsByName("csrfmiddlewaretoken");

dropdown.style.display = "none";
loading.style.display = "none";

const clearMessage = () => {
	setTimeout(() => {
		message.innerHTML = "";
	}, 5000);
};

const showMessage = (type = "info", text) => {
	message.innerHTML = "";
	const output = `
		<div class="alert alert-${type} alert-dismissible fade show" role="alert">
			${text}
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
		</div>
	`;
	message.innerHTML = output;
	clearMessage();
};

// fetch products
const fetchProducts = async () => {
	let response = await fetch("/api/v1/product");
	let data = await response.json();
	arr.push(...data);
};
fetchProducts();

// get customer
const getCustomer = async (phone) => {
	const url = `/api/v1/customer?phone=${phone}`;
	loading.style.display = "block";
	let response = await fetch(url);
	let data = await response.json();
	if (data.customer) {
		customerName.value = data?.customer?.name;
		customerId = data.customer.id;
	} else {
		customerName.value = "";
		showMessage("danger", "Customer not found.");
	}
	loading.style.display = "none";
};

// string to slug
const string_to_slug = (str) => {
	str = str.replace(/^\s+|\s+$/g, ""); // trim
	str = str.toLowerCase();

	// remove accents, swap ñ for n, etc
	let from = "àáãäâèéëêìíïîòóöôùúüûñç·/_,:;";
	let to = "aaaaaeeeeiiiioooouuuunc------";

	for (let i = 0, l = from.length; i < l; i++) {
		str = str.replace(new RegExp(from.charAt(i), "g"), to.charAt(i));
	}

	str = str
		.replace(/[^a-z0-9 -]/g, "") // remove invalid chars
		.replace(/\s+/g, "-") // collapse whitespace and replace by -
		.replace(/-+/g, "-"); // collapse dashes

	return str;
};

//shows the list
const show = () => {
	dropdown.style.display = "none";

	optionsVal.options.length = 0;

	if (input.value) {
		dropdown.style.display = "block";
		const textProduct = string_to_slug(input.value);

		for (let i = 0; i < arr.length; i++) {
			if (arr[i].product_slug.indexOf(textProduct) !== -1) {
				//addvalue
				addValue(arr[i].product_name, arr[i].id);
				optionsVal.size = optionsVal.options.length;
			}
		}
	}
};

//Settin the value in the box by firing the click event
const setVal = (text, val) => {
	console.log(text, val);

	input.value = text;
	productValue.value = val;
	const product = arr.find((item) => item.id === parseInt(val));
	productPrice.value = product.sell_price;
	productQuantity.value = product.quantity;
	document.getElementById("dropdown").style.display = "none";
};

const addValue = (text, val) => {
	const createOptions = document.createElement("option");
	// createOptions.setAttribute("onclick", "setVal(text, val)");
	createOptions.onclick = () => {
		setVal(text, val);
	};
	optionsVal.appendChild(createOptions);
	createOptions.text = text;
	createOptions.value = val;
};

// const filterCartItems = () => {
// 	ids = [];
// 	for (let i = 0; i < cart.length; i++) {
// 		ids.push(cart[i].id);
// 	}
// 	return arr.filter((item) => ids.includes(item.id));
// };

const showCartItems = () => {
	let output = "";
	showCart.forEach((item) => {
		output += `
			<tr>
				<td class="d-none">${item.id}</td>
				<td>${item.name}</td>
				<td>${item.price}</td>
				<td>${item.quantity}</td>
				<td style="width: 90px;">
					<button onclick="removeProductFromCart(${item.id})" type="button" class="btn btn-outline-danger btn-sm">
						<i class="fa fa-trash-alt"></i>
					</button>
				</td>
			</tr>
		`;
	});
	document.getElementById("cartData").innerHTML = output;
};

// add product to cart
const addProductToCart = () => {
	const product_id = parseInt(productValue.value);
	const product_price = parseFloat(productPrice.value);
	const product_quantity = parseInt(productQuantity.value);

	if (product_id !== "" && product_price > 0 && product_quantity > 0) {
		let product = {
			id: product_id,
			price: productPrice.value,
			quantity: productQuantity.value,
		};
		let showProduct = {
			id: product_id,
			name: input.value,
			price: product_price,
			quantity: product_quantity,
		};
		cart.push(product);
		showCart.push(showProduct);
		showCartItems();
		productValue.value = "";
		productPrice.value = "";
		productQuantity.value = "";
		input.value = "";
	} else {
		if (product_price <= 0) {
			showMessage("danger", "Invalid price.");
		} else if (product_quantity <= 0) {
			showMessage("danger", "Invalid quantity.");
		} else showMessage("danger", "Please select a product.");
	}

	console.log(cart);
};

// remove product to local storage
const removeProductFromCart = (productId) => {
	let products = cart.filter((product) => product.id !== productId);
	let showProducts = showCart.filter((product) => product.id !== productId);
	cart = products;
	showCart = showProducts;
	showCartItems();
};

// Event listeners
input.addEventListener("keyup", show);

// optionsVal.onclick = function () {
// 	setVal(this);
// };

// get customer trigger
customerPhone.onblur = () => {
	let phone = customerPhone.value;
	if (phone.length === 0) {
		customerName.value = "";
		return false;
	} else {
		if (phone.length === 11) {
			getCustomer(phone);
		} else {
			customerName.value = "";
			showMessage("danger", "Invalid phone number.");
		}
	}
};

sellSubmit.addEventListener("click", async () => {
	console.log("ok");
	const sellData = {
		customer_id: customerId,
		customer_name: customerName.value,
		customer_phone: customerPhone.value,
		sell_items: cart,
	};

	console.log("selldata", sellData);
	try {
		const config = {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				"X-CSRFToken": csrf[0].value,
			},
			body: JSON.stringify(sellData),
			credentials: "same-origin",
		};
		const response = await fetch(`/api/v1/sell`, config);

		if (response.status === 201) {
			const json = await response.json();
			console.log("json >>>", json);
			// reset form and clean errors
			// e.target.reset();
			// productModalClose.click();
			// displayError.classList.add("d-none");
		}
	} catch (error) {
		console.log(error);
	}
});
