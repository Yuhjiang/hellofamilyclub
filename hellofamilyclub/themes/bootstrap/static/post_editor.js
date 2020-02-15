window.onload = function($) {
    const content_md = document.getElementsByClassName('field-content_md')[0];
    const content_ck = document.getElementsByClassName('field-content_ck')[0];
    const is_md = document.getElementById('id_is_md');

    const switchEditor = (is_md) => {
        if (is_md.checked) {
            content_md.hidden = false;
            content_ck.hidden = true;
        } else {
            content_ck.hidden = false;
            content_md.hidden = true;
        }
    };

    is_md.onclick = function () {
        switchEditor(is_md);
    };
    switchEditor(is_md);
};