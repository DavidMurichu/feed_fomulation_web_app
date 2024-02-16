
    var name_count = 0;
    var feed_count=0;

    function increment() {
        name_count++;
        activate();
        document.getElementById('nameCountInput').value = name_count;
    }

    // function ad_nutrient() {
    //     var table = document.getElementsByClassName('nutrient_row');
    //     var firstTable = table[0];
    //     var newRow = document.createElement('tr');
    //     var newCell = document.createElement('td');
    //     var newInput = document.createElement('input');
    //     newInput.type = 'text';
    //     newInput.className = 'form-control';
    //     newInput.required = true;
    //     newInput.name = 'n_' + String(name_count);
    //     newCell.appendChild(newInput);
    //     var newCell1 = document.createElement('td');
    //     var newInput1 = document.createElement('input');
    //     newInput1.type = 'number';
    //     newInput1.step= 'any';
    //     newInput1.className = 'form-control';
    //     newInput1.required = true;
    //     newInput1.name = 'a_' + String(name_count);
    //     newCell1.appendChild(newInput1);
    //     newRow.appendChild(newCell);
    //     newRow.appendChild(newCell1);
    //     firstTable.appendChild(newRow);
    //     increment();
    // }

    function deleteLastRow() {
        var table = document.getElementsByClassName('nutrient_row');
        var firstTable = table[0];
        if (firstTable.rows.length > 0) {
            firstTable.deleteRow(firstTable.rows.length - 1);
            name_count--;
            activate();
            document.getElementById('nameCountInput').value = name_count;
        }
    }

    function activate() {
        var element = document.getElementById('submit');
        if (name_count === 0) {
            element.setAttribute('disabled', true);
        } else {
            element.removeAttribute('disabled');
        }
    }

    function checked(id) {
        var table = document.getElementsByClassName('ingridient_row');
        var firstTable = table[0];
        var newInput = document.createElement('input');
        newInput.type = 'hidden';
        newInput.value=id;
        newInput.id=id;
        newInput.className = 'form-control';
        newInput.required = true;
        newInput.name = 'feed' ;
        firstTable.appendChild(newInput);
    
    }
    

    function unchecked(id) {
        var row = document.getElementById(id);
        
        // Check if the row with the given id exists
        if (row) {
            // Get the parent node (which should be the table)
            var table = row.parentNode;
    
            // Remove the row from the table
            table.removeChild(row);
          
            
            // If you want to do something else when a row is deleted, you can add your logic here
        }
    }
    
    
 
    function checkboxChanged(id) {
        var checkbox = document.getElementById('myCheckbox_' + id);
    
        if (checkbox) {
            if (checkbox.checked) {
                checked(id);
                // Your logic when the checkbox is checked
            } else {
                unchecked(id);
                // Your logic when the checkbox is unchecked
            }
        }
    }
    
    activate();
