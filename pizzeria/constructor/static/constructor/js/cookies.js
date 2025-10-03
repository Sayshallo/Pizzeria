// SAUCE COOKIE
let sauce_id = '';
const parts = document.cookie.replace(/=/g, ' ').replace(/,/g, ' ').split(" ");

for (var i = 0; i < parts.length; i++) {
    if (parts[i] == 'sauce') {
        sauce_id = parts[i+1].replace(/;/g, '');
    }
}

if (sauce_id == ''){ document.getElementById('btn_sauce_2').click(); }
else {
    document.getElementById('btn_sauce_' + sauce_id.toString()).classList.add("green");
    document.getElementById('sauce_img_' + sauce_id.toString()).style.opacity = "1";
}

// FILLINGS COOKIE


elements = new Array();
// Get current cookie by 'Filling'
        for (var i = 0; i < parts.length; i++) {
            if (parts[i] == 'filling') {
                    for (var j = i+1; j < parts.length; j++) {
                        current_element = Number(parts[j].replace(/;/g, ''));
                        if (isNaN(current_element) == false) {
                            elements.push(current_element);
                        } else { break; }
                    }
            } else { continue; }
        }

if (elements.length > 0){
    for (var i = 0; i < elements.length; i++) {
        document.getElementById('btn_fill_' + elements[i].toString()).classList.add("green");
        document.getElementById('fill_img_' + elements[i].toString()).style.opacity = "1";
    }
}

