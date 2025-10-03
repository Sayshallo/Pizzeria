function add(elem) {
  fill_id = elem.id.split('_')[2];

  if(elem.id.split('_')[1] == 'fill') {
    current_img = document.getElementById('fill_img_'.concat(fill_id.toString()));

    if (elem.classList.contains("green") == false) {
        console.log('adding');
        elem.classList.add("green");
        current_img.style.opacity = "1";
        letHimCook(fill_id, 'filling', false);
    } else {
        console.log('removing');
        elem.classList.remove("green");
        current_img.style.opacity = "0";
        console.log('fill_id', fill_id)
        letHimCook(fill_id, 'filling', true);
    }
  }
  else {
    current_img = document.getElementById('sauce_img_'.concat(fill_id.toString()));

    var images = document.querySelectorAll('*[id^="sauce_img_"]');
    var buttons = document.querySelectorAll('*[id^="btn_sauce_"]');
    for (var i = 0; i < images.length; i++) {
     images.item(i).style.opacity = "0";
     buttons.item(i).classList.remove("green");
    }

    if (elem.classList.contains("green") == false) {
        elem.classList.add("green");
        current_img.style.opacity = "1";
        letHimCook(fill_id, 'sauce', false);
    } else {
        elem.classList.remove("green");
        current_img.style.opacity = "0";
    }
  }
}

function letHimCook(el_id, el_type, isSet) {
    // Searching all cookies
    const parts = document.cookie.replace(/=/g, ' ').replace(/,/g, ' ').split(" ");
    cookie_str = ''
    elements = new Array();

    // Get current cookie by 'Filling'
        for (var i = 0; i < parts.length; i++) {
            if (parts[i] == el_type) {
                if (el_type == 'filling') {
                    for (var j = i+1; j < parts.length; j++) {
                        current_element = Number(parts[j].replace(/;/g, ''));
                        if (isNaN(current_element) == false) {
                            elements.push(current_element);
                        } else { break; }
                    }
                }
            } else { continue; }
        }

    // Need to add / del
    if (isSet) {
        if (el_type == 'filling') {
            new_elements = removeNumber(elements, el_id);
            deleteCookie('filling');
            if (new_elements.length > 0) { document.cookie = "filling="+new_elements.join(' ')+";"; }
        }
    }
    else {
        console.log('ultra add');
        console.log('all cookies',parts)
        console.log('all fillings',elements)
        console.log('current fill',el_id)
        console.log('new cookie',"filling="+elements.join(' ') + " "+el_id+";")

        if (el_type == 'filling') {
            deleteCookie('filling')
            document.cookie = "filling="+elements.join(' ') + " "+el_id+";";
        } else {
            deleteCookie('sauce')
            document.cookie = "sauce="+el_id+";";
        }
    }
}

function deleteCookie(name) {
    console.log('deleting by', name);
  // Устанавливаем "просроченную" дату для куки, создавая своеобразный временной парадокс
  document.cookie = name + '=; Max-Age=0;';
}

function removeNumber(arr, num) {
    return arr.filter(item => item != num);
}