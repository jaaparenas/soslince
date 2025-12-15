const useMask = () => {

  const decimalPositive = (_scale:number=3, _radix:string=".", _max=999999999) => {
    return {
      mask: Number,
      min: 0,
      max: _max,
      scale: _scale,
      radix: _radix
    }
  }

  const decimal = (_scale:number=3, _radix:string=".", _max=999999999, _min=-999999999) => {
    return {
      mask: Number,
      min: _min,
      max: _max,
      scale: _scale,
      radix: _radix
    }
  }

  return {
    decimal,
    decimalPositive
  };
};
export default useMask;
