"""Format determinition
"""
import os
from typing import Any, Optional
import inspect, sys
import pandas as pd

from .errors import NoSignatureFileError, SignatureColumnsError
from .strategy import Strategy


class FormatDeterminer:
    def __init__(self, path: str) -> None:
        """
        FormatDeterminer constructor

        Args:
            path (str): Path to signature file with all criterias
            to choose strategy for implementing format
        """
        self._path = path
        self._df_sig = self._signature_to_df(self._path)
    
    def _signature_to_df(self, path: str) -> pd.DataFrame:
        ext = os.path.splitext(path)[1]

        if ext in ('.xls', '.xlsx'):
            pass
        else:
            raise NoSignatureFileError("There is no excel file with criterias")
        
        df = pd.read_excel(path) # Only for excel

        if ('format_type' in df.columns):
            return df
        else:
            msg = "There is no columns: format_type"
            raise SignatureColumnsError(msg)
    
    def define_strategy(self, text: str) -> Strategy:
        for row in self._df_sig.iterrows():
            strategy = self._row_strategy(text, row)
            if strategy is None:
                continue
            else:
                for cls in inspect.getmembers(sys.modules['pythoth.strategy'], inspect.isclass):
                    if cls[0] == strategy:
                        return cls[1]()
                    else:
                        continue
                raise NotImplementedError(f"Strategy {strategy} is not implemented")

    def _row_strategy(self, text: str, 
                      row: tuple[int, pd.Series]) -> Optional[str]:
        for col_name, col_val in row[1].items():
            check = self._validate(text,
                                   column_name=col_name, 
                                   column_value=col_val)
            if check is True:
                continue
            else:
                return None
            
        return row[1]['format_type']

    def _apply_rule(self, text: str, 
                    column_name: str, 
                    column_value: Any) -> bool:
        if column_name == 'format_type':
            return True
        else:
            # TODO: extend with some ruling patterns to substitute rule handling
            if str(column_value) in text:
                return True
            else:
                return False

    def _validate(self, text: str, 
                  column_name: str, 
                  column_value: Any) -> bool:
        return self._apply_rule(text, column_name, column_value)
    

if __name__ == '__main__':
    fd = FormatDeterminer(path='signature.xlsx')
    res = fd.define_strategy('DELLDIRECT is 54654 important Document type you need name his NAME and pass through 555')
    print(res)