from django.shortcuts import redirect

def SessionCheck(get_response):
    def middleware(request):        
        url = request.get_full_path()
        if "myuser/" in url:
            if 'loginuser' not in request.session:
                return redirect('/login')
        elif "admin/" in url:
            response = get_response(request)
            return response
        else:    
            if 'loginuser' in request.session:
                return redirect('/myuser/home')
        response = get_response(request)
        return response
    return middleware