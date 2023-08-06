$(function(){
    $('input').on('click', function(){
        $(this).select();
    });

    var getFormData = function(selector){
        var arr = $(selector).serializeArray();
        var json = arr.reduce(function (obj, it) { obj[it.name] = it.value; return obj }, {})
        return encodeURIComponent(JSON.stringify(json));
    }
    $('#btn-reset').on('click', function(){
        $('#filter-form input').val('');
        $('#filter-form textarea').val('');
        $(".chosen-select").val('').trigger("chosen:updated");

        $('#filter-form').submit();
    });

    // $('#filter-form').on('submit',function(event){
    //     event.preventDefault();
    //     $('#submit-form-filter').val(getFormData('#filter-form'));
    //     $('#submit-form').submit();
    // });

    $(".chosen-select").chosen({
        no_results_text: "Nenhum resultado encontrado: ",
        allow_single_deselect: true
    }).change(function(){
        var target = this.dataset.name;
        var values = $("option:selected", this).map(function () { return this.value }).get().join(",");
        $('[name="'+ target +'"]').val(values);
        console.log($('[name="' + target + '"]').val());
    }).trigger('change');



    $('.number-format').change(function(){
        var val = this.value;
        var name = this.dataset.name;
        var format = this.dataset.format || '0';
        var numberPattern = /^\d+[.]?\d+$/g;

        if (numberPattern.test(val)) {
            val = parseFloat(val);
        }
        if (val !== '') {
            this.value = numeral(val).format(format)
            $('[name="' + name + '"]').val(numeral(val).value())
        }
    });

    $('.date-format').change(function(event, isInit){
        var val = this.value;
        var name = this.dataset.name;
        var format = this.dataset.format || 'DD/MM/YYYY';
        var formatOut = this.dataset.format_out || 'YYYY-MM-DD'
        this.value = moment(val, (isInit ? formatOut : format)).format(format).replace('Invalid date', '');
        $('[name="' + name + '"]').val(moment(this.value, format).format(formatOut).replace('Invalid date', ''));
    }).trigger('change',[true]);



    // Print filter
    var printFilters = $('#filter-form label').map(function () {
        var label = $(this).text();
        var value = $(this).siblings(':first').val();
        return value ? '<b>'+label + '</b>: ' + value : '';
    }).get().filter(Boolean).join(', ');

    $('#print-filter').html(printFilters);
    $('#print-filter-title').html('Em ' + moment().format('DD/MM/YYYY HH:mm') + (printFilters ? ', Filtrado por:' : ''))

    var $table = $('table').bootstrapTable({
        paginate: false,
        cache: false,
        search: false,
        locale: 'pt-BR',
        // showColumns: true,
        iconSize: 'sm',
        // cookie: true,
        // cookieIdTable: 'saveId',
        // cookiesEnabled: ['bs.table.columns'],
        customSort: function(sortName, sortOrder, data){
            var order = (sortOrder === 'desc' ? '-' : '') + sortName
            $('[name="filter._order"]').val(order);
            if (initialNameOrder.length > 0) {
                initialNameOrder = ''
                return 0;
            }
            $('#filter-form').submit();
            return 0;
        },
        sortClass: 'table-active',
    });
    var initialNameOrder = ($('[name="filter._order"]').val() || '').replace(/^-/, 'desc ').split(' ').reverse().filter(Boolean);
    $table.bootstrapTable('refreshOptions', {
        sortName: initialNameOrder[0],
        sortOrder: initialNameOrder[1]
    })
    $('button.dropdown-toggle').addClass('d-print-none');

    $('.form-control:first').focus().select();
});