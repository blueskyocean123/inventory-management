// =====================
// calculate total price
// =====================
const id_quantity = document.getElementById("id_quantity");
const id_price = document.getElementById("id_price");
const totalPrice = document.getElementById("totalPrice");
const showTotal = document.getElementById("showTotal");
showTotal.style.display = "none";

const calculateTotalPrice = () => {
	const total = id_price.value * id_quantity.value;
	totalPrice.innerHTML = total;

	if (total > 0) {
		showTotal.style.display = "block";
	} else {
		showTotal.style.display = "none";
	}
};

id_price.addEventListener("change", calculateTotalPrice);
id_quantity.addEventListener("change", calculateTotalPrice);

// ===============
// add new product
// ===============
const productSelect = document.getElementById("id_product");
const productModalClose = document.getElementById("productModalClose");
const newProductForm = document.getElementById("newProductForm");
const displayError = document.getElementById("displayError");

const csrf = document.getElementsByName("csrfmiddlewaretoken");

const saveNewProduct = async (e) => {
	e.preventDefault();
	displayError.classList.add("d-none");

	const newProduct = document.getElementById("newProduct").value;
	const data = { product_name: newProduct };
	try {
		const config = {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				"X-CSRFToken": csrf[0].value,
			},
			body: JSON.stringify(data),
			credentials: "same-origin",
		};
		const response = await fetch("/api/v1/product", config);

		if (response.status === 201) {
			const json = await response.json();
			console.log("json >>>", json);
			// reset form and clean errors
			e.target.reset();
			productModalClose.click();
			displayError.classList.add("d-none");

			// add product to options
			const newProductOption = document.createElement("option");
			newProductOption.text = json.product_name;
			newProductOption.value = parseInt(json.id);
			productSelect.add(newProductOption);
		}

		if (response.status === 400) {
			const json = await response.json();
			displayError.classList.remove("d-none");
			document.getElementById(
				"errorText"
			).innerHTML = `${json.product_name[0]}`;
		}
	} catch (error) {
		displayError.classList.remove("d-none");
		document.getElementById("errorText").innerHTML = "Network error!!!";
	}
};

newProductForm.addEventListener("submit", saveNewProduct);
