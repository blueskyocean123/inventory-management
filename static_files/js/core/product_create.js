let subcategories = [];

// fetch subcategories
const fetchSubcategories = async () => {
	let response = await fetch("/api/v1/subcategory");
	let data = await response.json();
	subcategories.push(...data);
};
fetchSubcategories();

// select subcategory onChange
const selectSubcategory = () => {
	const category = document.getElementById("id_category");
	const subCategory = document.getElementById("id_subcategory");
	const categoryValue = category.options[category.selectedIndex].value;
	const returnedSubcats = subcategories.filter(
		(subcat) => subcat.category == parseInt(categoryValue)
	);
	let output = "";
	for (const item of returnedSubcats) {
		output += `
            <option value="${item.id}">${item.name}</option>
        `;
	}
	subCategory.innerHTML = output;
};
