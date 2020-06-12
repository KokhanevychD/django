$('#listbutton').click(function(){

    $.ajax({
        type:'GET',
        url:'/api/articles',
        success: function(data){

            let container = $('.alert:first').clone();
            let tag = $('.tags:first').clone()
            container.find('.tagsdiv').empty();
            $('.articlelist').empty();

            for (idx in data.results) {
                current_data = data.results[idx]
                let clone = container.clone().css('display', '');
                clone.find('.title').text(current_data.title);

                for (idx in current_data.tags){
                    item = current_data.tags[idx]
                    let new_tag = tag.clone();
                    new_tag.find('.badge').text(item.name)
                    new_tag.appendTo(clone.find('.tagsdiv'))
                };

                clone.find('.content').text(current_data.content);
                clone.find('.author').text(current_data.author.username);
                clone.find('.postdate').text(current_data.post_date);
                clone.appendTo('.articlelist');

            }

        }

    })

})
