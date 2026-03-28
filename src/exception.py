import sys
# import logging

def error_message_detail(error,error_detail:sys): # jo bhi error aaye mai usse apne own custom message me push krna hai mujhe 
    _,_,exc_tb = error_detail.exc_info() # basically gives 3 info pehle 2 se kaam nhi hai 3rd is important .tb waala ye btata hai kis file me kis line me rror hai
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name {} line number {} error message {}".format(file_name,exc_tb.tb_lineno,str(error))
                                                                                                    
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
# if __name__== '__main__':
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Divide by zero")
#         raise CustomException(e,sys)    