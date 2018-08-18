    function convert(currencies) {
        var select_1 = document.getElementById("currency_1");
        var select_2 = document.getElementById("currency_2");
        var amount_box = document.getElementById("amount");
        if (select_1[select_1.selectedIndex].value !== "empty" && select_2[select_2.selectedIndex].value !== "empty" && amount_box.value !== "" && amount_box.value !== null) {
            var from_currency = select_1[select_1.selectedIndex];
            var to_currency = select_2[select_2.selectedIndex];
            var amount_to_convert = parseFloat(amount_box.value);
            var from_dic;
            switch(from_currency.value) {
                case "rial":
                    from_dic = currencies[0];
                    break;
                case "dollar":
                    from_dic = currencies[1];
                    break;
                case "euro":
                    from_dic = currencies[2];
                    break;
                default:
                    break;
            }
            var multiplicand;
            switch(to_currency.value) {
                case "rial":
                    multiplicand = parseFloat(from_dic.rial_value);
                    break;
                case "dollar":
                    multiplicand = parseFloat(from_dic.dollar_value);
                    break;
                case "euro":
                    multiplicand = parseFloat(from_dic.euro_value);
                    break;
                default:
                    break;
            }
            var conversion_res;
            conversion_res = multiplicand * parseFloat(amount_box.value);
            document.getElementById("cc-amount").value = conversion_res;
        } else {
            alert("Please fill all the inputs.");
        }
    }