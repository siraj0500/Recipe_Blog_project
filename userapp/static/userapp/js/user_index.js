/*--==Scroll-bar-script======================-*/
 
    let scrollPercentage = () => {
        let scrollProgress = document.getElementById("progress");
        let progressValue = document.getElementById("progress-value");
        let pos = document.documentElement.scrollTop;
        let calcHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        let scrollValue = Math.round( pos * 100 / calcHeight);
        scrollProgress.style.background = `conic-gradient(#e2d30c ${scrollValue}%, #2b2f38 ${scrollValue}%)`;
        progressValue.textcontent = `${scrollValue}%`;
 
    }
    window.onscroll = scrollPercentage;
    window.onload = scrollPercentage;
 
 
    /*--==Post-Filter-Script=================================--*/
    
        $(document).on('click','.blog-filter li', function(){
            $(this).addClass('blog-filter-active').siblings().removeClass('blog-filter-active')
        });
 
        /*--filter------------------------*/
        $(document).ready(function(){
            $('.list').click(function(){
                const value = $(this).attr('data-filter');
                if(value === 'all'){
                    $('.blog-box').show('1000');
                }
                else{
                    $('.blog-box').not('.'+value).hide('1000');
                }
            });
        });
 