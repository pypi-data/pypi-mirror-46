#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/int_.hpp>
#include <pythonic/include/__builtin__/max.hpp>
#include <pythonic/include/__builtin__/min.hpp>
#include <pythonic/include/__builtin__/pythran/make_shape.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/float32.hpp>
#include <pythonic/include/numpy/sqrt.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/idiv.hpp>
#include <pythonic/include/operator_/ifloordiv.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/int_.hpp>
#include <pythonic/__builtin__/max.hpp>
#include <pythonic/__builtin__/min.hpp>
#include <pythonic/__builtin__/pythran/make_shape.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/float32.hpp>
#include <pythonic/numpy/sqrt.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/idiv.hpp>
#include <pythonic/operator_/ifloordiv.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_correl_pythran
{
  struct correl_pythran
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::int_{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
      typedef decltype(std::declval<__type2>()(std::declval<__type3>())) __type4;
      typedef long __type5;
      typedef decltype((pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>()))) __type6;
      typedef decltype((pythonic::operator_::add(std::declval<__type6>(), std::declval<__type5>()))) __type7;
      typedef typename pythonic::lazy<__type7>::type __type8;
      typedef decltype(std::declval<__type1>()(std::declval<__type8>(), std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float32{})>::type>::type __type10;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type9>(), std::declval<__type10>()))>::type __type11;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type12;
      typedef decltype((pythonic::operator_::add(std::declval<__type3>(), std::declval<__type5>()))) __type13;
      typedef decltype(std::declval<__type12>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type15>())) __type16;
      typedef indexable<__type16> __type17;
      typedef typename __combined<__type11,__type17>::type __type18;
      typedef decltype(std::declval<__type12>()(std::declval<__type3>())) __type19;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
      typedef decltype((pythonic::operator_::add(std::declval<__type20>(), std::declval<__type3>()))) __type21;
      typedef decltype((pythonic::operator_::add(std::declval<__type21>(), std::declval<__type5>()))) __type22;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type22>())) __type23;
      typedef indexable<__type23> __type24;
      typedef typename __combined<__type18,__type24>::type __type25;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type15>())) __type26;
      typedef indexable<__type26> __type27;
      typedef typename __combined<__type25,__type27>::type __type28;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type22>())) __type29;
      typedef indexable<__type29> __type30;
      typedef typename __combined<__type28,__type30>::type __type31;
      typedef typename pythonic::assignable<double>::type __type32;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type33;
      typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type33>())) __type34;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type34>::type>::type>::type __type35;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::min{})>::type>::type __type36;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type37;
      typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type37>())) __type38;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type38>::type>::type>::type __type39;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type39>(), std::declval<__type5>()))) __type40;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type35>(), std::declval<__type5>()))) __type41;
      typedef decltype((std::declval<__type40>() - std::declval<__type41>())) __type42;
      typedef decltype((-std::declval<__type3>())) __type43;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type43>(), std::declval<__type15>())))>::type __type44;
      typedef decltype((pythonic::operator_::add(std::declval<__type42>(), std::declval<__type44>()))) __type45;
      typedef decltype(std::declval<__type36>()(std::declval<__type45>(), std::declval<__type5>())) __type46;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type35>(), std::declval<__type46>())))>::type __type47;
      typedef decltype(std::declval<__type12>()(std::declval<__type47>())) __type48;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type48>::type::iterator>::value_type>::type __type49;
      typedef typename pythonic::assignable<decltype((-std::declval<__type46>()))>::type __type50;
      typedef decltype((pythonic::operator_::add(std::declval<__type49>(), std::declval<__type50>()))) __type51;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type34>::type>::type>::type __type52;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type38>::type>::type>::type __type53;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type53>(), std::declval<__type5>()))) __type54;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type52>(), std::declval<__type5>()))) __type55;
      typedef decltype((std::declval<__type54>() - std::declval<__type55>())) __type56;
      typedef decltype((pythonic::operator_::add(std::declval<__type56>(), std::declval<__type44>()))) __type57;
      typedef decltype(std::declval<__type36>()(std::declval<__type57>(), std::declval<__type5>())) __type58;
      typedef decltype((pythonic::operator_::add(std::declval<__type52>(), std::declval<__type58>()))) __type59;
      typedef decltype(std::declval<__type12>()(std::declval<__type59>())) __type60;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type60>::type::iterator>::value_type>::type __type61;
      typedef typename pythonic::assignable<decltype((-std::declval<__type58>()))>::type __type62;
      typedef decltype((pythonic::operator_::add(std::declval<__type61>(), std::declval<__type62>()))) __type63;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type63>())) __type64;
      typedef decltype(std::declval<__type33>()[std::declval<__type64>()]) __type65;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type __type66;
      typedef typename pythonic::assignable<decltype(std::declval<__type66>()(std::declval<__type5>(), std::declval<__type45>()))>::type __type67;
      typedef decltype((pythonic::operator_::add(std::declval<__type67>(), std::declval<__type49>()))) __type68;
      typedef typename pythonic::assignable<decltype(std::declval<__type66>()(std::declval<__type5>(), std::declval<__type57>()))>::type __type69;
      typedef decltype((pythonic::operator_::add(std::declval<__type69>(), std::declval<__type61>()))) __type70;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type68>(), std::declval<__type70>())) __type71;
      typedef decltype(std::declval<__type37>()[std::declval<__type71>()]) __type72;
      typedef decltype((pythonic::operator_::mul(std::declval<__type65>(), std::declval<__type72>()))) __type73;
      typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type73>()))) __type74;
      typedef typename __combined<__type32,__type74>::type __type75;
      typedef typename __combined<__type75,__type73>::type __type76;
      typedef decltype((pythonic::operator_::add(std::declval<__type59>(), std::declval<__type52>()))) __type77;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type54>(), std::declval<__type53>()))) __type78;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type78>(), std::declval<__type5>()))) __type79;
      typedef decltype((std::declval<__type56>() - std::declval<__type79>())) __type80;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type55>(), std::declval<__type52>()))) __type81;
      typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type81>(), std::declval<__type5>()))) __type82;
      typedef decltype((std::declval<__type80>() - std::declval<__type82>())) __type83;
      typedef decltype((pythonic::operator_::add(std::declval<__type57>(), std::declval<__type83>()))) __type84;
      typedef decltype((pythonic::operator_::add(std::declval<__type84>(), std::declval<__type44>()))) __type85;
      typedef decltype(std::declval<__type36>()(std::declval<__type85>(), std::declval<__type5>())) __type86;
      typedef decltype((pythonic::operator_::add(std::declval<__type77>(), std::declval<__type86>()))) __type87;
      typedef decltype((pythonic::operator_::mul(std::declval<__type87>(), std::declval<__type47>()))) __type88;
      typedef decltype((pythonic::operator_::div(std::declval<__type76>(), std::declval<__type88>()))) __type89;
      typedef container<typename std::remove_reference<__type89>::type> __type90;
      typedef typename __combined<__type31,__type90>::type __type91;
      typedef typename __combined<__type91,__type17>::type __type92;
      typedef typename __combined<__type92,__type90>::type __type93;
      typedef decltype((pythonic::operator_::add(std::declval<__type54>(), std::declval<__type55>()))) __type94;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type20>(), std::declval<__type5>())))>::type __type95;
      typedef decltype((pythonic::operator_::add(std::declval<__type94>(), std::declval<__type95>()))) __type96;
      typedef decltype((std::declval<__type96>() - std::declval<__type53>())) __type97;
      typedef decltype(std::declval<__type66>()(std::declval<__type97>(), std::declval<__type5>())) __type98;
      typedef decltype((std::declval<__type52>() - std::declval<__type98>())) __type99;
      typedef decltype(std::declval<__type12>()(std::declval<__type99>())) __type100;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type100>::type::iterator>::value_type>::type __type101;
      typedef decltype((pythonic::operator_::add(std::declval<__type101>(), std::declval<__type5>()))) __type102;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type102>())) __type103;
      typedef decltype(std::declval<__type33>()[std::declval<__type103>()]) __type104;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type56>(), std::declval<__type95>())))>::type __type105;
      typedef decltype((pythonic::operator_::add(std::declval<__type105>(), std::declval<__type101>()))) __type106;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type68>(), std::declval<__type106>())) __type107;
      typedef decltype(std::declval<__type37>()[std::declval<__type107>()]) __type108;
      typedef decltype((pythonic::operator_::mul(std::declval<__type104>(), std::declval<__type108>()))) __type109;
      typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type109>()))) __type110;
      typedef typename __combined<__type32,__type110>::type __type111;
      typedef typename __combined<__type111,__type109>::type __type112;
      typedef decltype((std::declval<__type99>() - std::declval<__type52>())) __type113;
      typedef decltype((pythonic::operator_::add(std::declval<__type94>(), std::declval<__type79>()))) __type114;
      typedef decltype((pythonic::operator_::add(std::declval<__type114>(), std::declval<__type82>()))) __type115;
      typedef decltype((pythonic::operator_::add(std::declval<__type96>(), std::declval<__type115>()))) __type116;
      typedef decltype((pythonic::operator_::add(std::declval<__type116>(), std::declval<__type95>()))) __type117;
      typedef decltype((std::declval<__type97>() - std::declval<__type117>())) __type118;
      typedef decltype((std::declval<__type118>() - std::declval<__type53>())) __type119;
      typedef decltype(std::declval<__type66>()(std::declval<__type119>(), std::declval<__type5>())) __type120;
      typedef decltype((std::declval<__type113>() - std::declval<__type120>())) __type121;
      typedef decltype((pythonic::operator_::mul(std::declval<__type121>(), std::declval<__type47>()))) __type122;
      typedef decltype((pythonic::operator_::div(std::declval<__type112>(), std::declval<__type122>()))) __type123;
      typedef container<typename std::remove_reference<__type123>::type> __type124;
      typedef typename __combined<__type93,__type124>::type __type125;
      typedef typename __combined<__type125,__type24>::type __type126;
      typedef typename __combined<__type126,__type124>::type __type127;
      typedef decltype((pythonic::operator_::add(std::declval<__type40>(), std::declval<__type41>()))) __type128;
      typedef decltype((pythonic::operator_::add(std::declval<__type128>(), std::declval<__type95>()))) __type129;
      typedef decltype((std::declval<__type129>() - std::declval<__type39>())) __type130;
      typedef decltype(std::declval<__type66>()(std::declval<__type130>(), std::declval<__type5>())) __type131;
      typedef typename pythonic::assignable<decltype((std::declval<__type35>() - std::declval<__type131>()))>::type __type132;
      typedef decltype(std::declval<__type12>()(std::declval<__type132>())) __type133;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type133>::type::iterator>::value_type>::type __type134;
      typedef decltype((pythonic::operator_::add(std::declval<__type134>(), std::declval<__type5>()))) __type135;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type135>(), std::declval<__type63>())) __type136;
      typedef decltype(std::declval<__type33>()[std::declval<__type136>()]) __type137;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type42>(), std::declval<__type95>())))>::type __type138;
      typedef decltype((pythonic::operator_::add(std::declval<__type138>(), std::declval<__type134>()))) __type139;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type139>(), std::declval<__type70>())) __type140;
      typedef decltype(std::declval<__type37>()[std::declval<__type140>()]) __type141;
      typedef decltype((pythonic::operator_::mul(std::declval<__type137>(), std::declval<__type141>()))) __type142;
      typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type142>()))) __type143;
      typedef typename __combined<__type32,__type143>::type __type144;
      typedef typename __combined<__type144,__type142>::type __type145;
      typedef decltype((pythonic::operator_::mul(std::declval<__type87>(), std::declval<__type132>()))) __type146;
      typedef decltype((pythonic::operator_::div(std::declval<__type145>(), std::declval<__type146>()))) __type147;
      typedef container<typename std::remove_reference<__type147>::type> __type148;
      typedef typename __combined<__type127,__type148>::type __type149;
      typedef typename __combined<__type149,__type27>::type __type150;
      typedef typename __combined<__type150,__type148>::type __type151;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type135>(), std::declval<__type102>())) __type152;
      typedef decltype(std::declval<__type33>()[std::declval<__type152>()]) __type153;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type139>(), std::declval<__type106>())) __type154;
      typedef decltype(std::declval<__type37>()[std::declval<__type154>()]) __type155;
      typedef decltype((pythonic::operator_::mul(std::declval<__type153>(), std::declval<__type155>()))) __type156;
      typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type156>()))) __type157;
      typedef typename __combined<__type32,__type157>::type __type158;
      typedef typename __combined<__type158,__type156>::type __type159;
      typedef decltype((pythonic::operator_::mul(std::declval<__type121>(), std::declval<__type132>()))) __type160;
      typedef decltype((pythonic::operator_::div(std::declval<__type159>(), std::declval<__type160>()))) __type161;
      typedef container<typename std::remove_reference<__type161>::type> __type162;
      typedef typename __combined<__type151,__type162>::type __type163;
      typedef typename __combined<__type163,__type30>::type __type164;
      typedef typename __combined<__type164,__type162>::type __type165;
      typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SIZE{}, std::declval<__type33>())) __type166;
      typedef decltype((pythonic::operator_::mul(std::declval<__type165>(), std::declval<__type166>()))) __type167;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sqrt{})>::type>::type __type168;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type169;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type170;
      typedef decltype(std::declval<__type170>()(std::declval<__type33>())) __type171;
      typedef decltype(std::declval<__type169>()(std::declval<__type171>())) __type172;
      typedef decltype(std::declval<__type170>()(std::declval<__type37>())) __type173;
      typedef decltype(std::declval<__type169>()(std::declval<__type173>())) __type174;
      typedef decltype((pythonic::operator_::mul(std::declval<__type172>(), std::declval<__type174>()))) __type175;
      typedef decltype(std::declval<__type168>()(std::declval<__type175>())) __type176;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type167>(), std::declval<__type176>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& im0, argument_type1&& im1, argument_type2&& disp_max) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename correl_pythran::type<argument_type0, argument_type1, argument_type2>::result_type correl_pythran::operator()(argument_type0&& im0, argument_type1&& im1, argument_type2&& disp_max) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::int_{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
    typedef decltype(std::declval<__type2>()(std::declval<__type3>())) __type4;
    typedef long __type5;
    typedef decltype((pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>()))) __type6;
    typedef decltype((pythonic::operator_::add(std::declval<__type6>(), std::declval<__type5>()))) __type7;
    typedef typename pythonic::lazy<__type7>::type __type8;
    typedef decltype(std::declval<__type1>()(std::declval<__type8>(), std::declval<__type8>())) __type9;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float32{})>::type>::type __type10;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type9>(), std::declval<__type10>()))>::type __type11;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type12;
    typedef decltype((pythonic::operator_::add(std::declval<__type3>(), std::declval<__type5>()))) __type13;
    typedef decltype(std::declval<__type12>()(std::declval<__type13>())) __type14;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type15>())) __type16;
    typedef indexable<__type16> __type17;
    typedef typename __combined<__type11,__type17>::type __type18;
    typedef decltype(std::declval<__type12>()(std::declval<__type3>())) __type19;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
    typedef decltype((pythonic::operator_::add(std::declval<__type20>(), std::declval<__type3>()))) __type21;
    typedef decltype((pythonic::operator_::add(std::declval<__type21>(), std::declval<__type5>()))) __type22;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type22>())) __type23;
    typedef indexable<__type23> __type24;
    typedef typename __combined<__type18,__type24>::type __type25;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type15>())) __type26;
    typedef indexable<__type26> __type27;
    typedef typename __combined<__type25,__type27>::type __type28;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type22>())) __type29;
    typedef indexable<__type29> __type30;
    typedef typename __combined<__type28,__type30>::type __type31;
    typedef typename pythonic::assignable<double>::type __type32;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type33;
    typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type33>())) __type34;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type34>::type>::type>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::min{})>::type>::type __type36;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type37;
    typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type37>())) __type38;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type38>::type>::type>::type __type39;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type39>(), std::declval<__type5>()))) __type40;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type35>(), std::declval<__type5>()))) __type41;
    typedef decltype((std::declval<__type40>() - std::declval<__type41>())) __type42;
    typedef decltype((-std::declval<__type3>())) __type43;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type43>(), std::declval<__type15>())))>::type __type44;
    typedef decltype((pythonic::operator_::add(std::declval<__type42>(), std::declval<__type44>()))) __type45;
    typedef decltype(std::declval<__type36>()(std::declval<__type45>(), std::declval<__type5>())) __type46;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type35>(), std::declval<__type46>())))>::type __type47;
    typedef decltype(std::declval<__type12>()(std::declval<__type47>())) __type48;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type48>::type::iterator>::value_type>::type __type49;
    typedef typename pythonic::assignable<decltype((-std::declval<__type46>()))>::type __type50;
    typedef decltype((pythonic::operator_::add(std::declval<__type49>(), std::declval<__type50>()))) __type51;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type34>::type>::type>::type __type52;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type38>::type>::type>::type __type53;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type53>(), std::declval<__type5>()))) __type54;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type52>(), std::declval<__type5>()))) __type55;
    typedef decltype((std::declval<__type54>() - std::declval<__type55>())) __type56;
    typedef decltype((pythonic::operator_::add(std::declval<__type56>(), std::declval<__type44>()))) __type57;
    typedef decltype(std::declval<__type36>()(std::declval<__type57>(), std::declval<__type5>())) __type58;
    typedef decltype((pythonic::operator_::add(std::declval<__type52>(), std::declval<__type58>()))) __type59;
    typedef decltype(std::declval<__type12>()(std::declval<__type59>())) __type60;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type60>::type::iterator>::value_type>::type __type61;
    typedef typename pythonic::assignable<decltype((-std::declval<__type58>()))>::type __type62;
    typedef decltype((pythonic::operator_::add(std::declval<__type61>(), std::declval<__type62>()))) __type63;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type63>())) __type64;
    typedef decltype(std::declval<__type33>()[std::declval<__type64>()]) __type65;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type __type66;
    typedef typename pythonic::assignable<decltype(std::declval<__type66>()(std::declval<__type5>(), std::declval<__type45>()))>::type __type67;
    typedef decltype((pythonic::operator_::add(std::declval<__type67>(), std::declval<__type49>()))) __type68;
    typedef typename pythonic::assignable<decltype(std::declval<__type66>()(std::declval<__type5>(), std::declval<__type57>()))>::type __type69;
    typedef decltype((pythonic::operator_::add(std::declval<__type69>(), std::declval<__type61>()))) __type70;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type68>(), std::declval<__type70>())) __type71;
    typedef decltype(std::declval<__type37>()[std::declval<__type71>()]) __type72;
    typedef decltype((pythonic::operator_::mul(std::declval<__type65>(), std::declval<__type72>()))) __type73;
    typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type73>()))) __type74;
    typedef typename __combined<__type32,__type74>::type __type75;
    typedef typename __combined<__type75,__type73>::type __type76;
    typedef decltype((pythonic::operator_::add(std::declval<__type59>(), std::declval<__type52>()))) __type77;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type54>(), std::declval<__type53>()))) __type78;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type78>(), std::declval<__type5>()))) __type79;
    typedef decltype((std::declval<__type56>() - std::declval<__type79>())) __type80;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type55>(), std::declval<__type52>()))) __type81;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type81>(), std::declval<__type5>()))) __type82;
    typedef decltype((std::declval<__type80>() - std::declval<__type82>())) __type83;
    typedef decltype((pythonic::operator_::add(std::declval<__type57>(), std::declval<__type83>()))) __type84;
    typedef decltype((pythonic::operator_::add(std::declval<__type84>(), std::declval<__type44>()))) __type85;
    typedef decltype(std::declval<__type36>()(std::declval<__type85>(), std::declval<__type5>())) __type86;
    typedef decltype((pythonic::operator_::add(std::declval<__type77>(), std::declval<__type86>()))) __type87;
    typedef decltype((pythonic::operator_::mul(std::declval<__type87>(), std::declval<__type47>()))) __type88;
    typedef decltype((pythonic::operator_::div(std::declval<__type76>(), std::declval<__type88>()))) __type89;
    typedef container<typename std::remove_reference<__type89>::type> __type90;
    typedef typename __combined<__type31,__type90>::type __type91;
    typedef typename __combined<__type91,__type17>::type __type92;
    typedef decltype((pythonic::operator_::add(std::declval<__type54>(), std::declval<__type55>()))) __type93;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type20>(), std::declval<__type5>())))>::type __type94;
    typedef decltype((pythonic::operator_::add(std::declval<__type93>(), std::declval<__type94>()))) __type95;
    typedef decltype((std::declval<__type95>() - std::declval<__type53>())) __type96;
    typedef decltype(std::declval<__type66>()(std::declval<__type96>(), std::declval<__type5>())) __type97;
    typedef decltype((std::declval<__type52>() - std::declval<__type97>())) __type98;
    typedef decltype(std::declval<__type12>()(std::declval<__type98>())) __type99;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type99>::type::iterator>::value_type>::type __type100;
    typedef decltype((pythonic::operator_::add(std::declval<__type100>(), std::declval<__type5>()))) __type101;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type101>())) __type102;
    typedef decltype(std::declval<__type33>()[std::declval<__type102>()]) __type103;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type56>(), std::declval<__type94>())))>::type __type104;
    typedef decltype((pythonic::operator_::add(std::declval<__type104>(), std::declval<__type100>()))) __type105;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type68>(), std::declval<__type105>())) __type106;
    typedef decltype(std::declval<__type37>()[std::declval<__type106>()]) __type107;
    typedef decltype((pythonic::operator_::mul(std::declval<__type103>(), std::declval<__type107>()))) __type108;
    typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type108>()))) __type109;
    typedef typename __combined<__type32,__type109>::type __type110;
    typedef typename __combined<__type110,__type108>::type __type111;
    typedef decltype((std::declval<__type98>() - std::declval<__type52>())) __type112;
    typedef decltype((pythonic::operator_::add(std::declval<__type93>(), std::declval<__type79>()))) __type113;
    typedef decltype((pythonic::operator_::add(std::declval<__type113>(), std::declval<__type82>()))) __type114;
    typedef decltype((pythonic::operator_::add(std::declval<__type95>(), std::declval<__type114>()))) __type115;
    typedef decltype((pythonic::operator_::add(std::declval<__type115>(), std::declval<__type94>()))) __type116;
    typedef decltype((std::declval<__type96>() - std::declval<__type116>())) __type117;
    typedef decltype((std::declval<__type117>() - std::declval<__type53>())) __type118;
    typedef decltype(std::declval<__type66>()(std::declval<__type118>(), std::declval<__type5>())) __type119;
    typedef decltype((std::declval<__type112>() - std::declval<__type119>())) __type120;
    typedef decltype((pythonic::operator_::mul(std::declval<__type120>(), std::declval<__type47>()))) __type121;
    typedef decltype((pythonic::operator_::div(std::declval<__type111>(), std::declval<__type121>()))) __type122;
    typedef container<typename std::remove_reference<__type122>::type> __type123;
    typedef typename __combined<__type92,__type123>::type __type124;
    typedef typename __combined<__type124,__type24>::type __type125;
    typedef decltype((pythonic::operator_::add(std::declval<__type40>(), std::declval<__type41>()))) __type126;
    typedef decltype((pythonic::operator_::add(std::declval<__type126>(), std::declval<__type94>()))) __type127;
    typedef decltype((std::declval<__type127>() - std::declval<__type39>())) __type128;
    typedef decltype(std::declval<__type66>()(std::declval<__type128>(), std::declval<__type5>())) __type129;
    typedef typename pythonic::assignable<decltype((std::declval<__type35>() - std::declval<__type129>()))>::type __type130;
    typedef decltype(std::declval<__type12>()(std::declval<__type130>())) __type131;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type131>::type::iterator>::value_type>::type __type132;
    typedef decltype((pythonic::operator_::add(std::declval<__type132>(), std::declval<__type5>()))) __type133;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type133>(), std::declval<__type63>())) __type134;
    typedef decltype(std::declval<__type33>()[std::declval<__type134>()]) __type135;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::add(std::declval<__type42>(), std::declval<__type94>())))>::type __type136;
    typedef decltype((pythonic::operator_::add(std::declval<__type136>(), std::declval<__type132>()))) __type137;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type137>(), std::declval<__type70>())) __type138;
    typedef decltype(std::declval<__type37>()[std::declval<__type138>()]) __type139;
    typedef decltype((pythonic::operator_::mul(std::declval<__type135>(), std::declval<__type139>()))) __type140;
    typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type140>()))) __type141;
    typedef typename __combined<__type32,__type141>::type __type142;
    typedef typename __combined<__type142,__type140>::type __type143;
    typedef decltype((pythonic::operator_::mul(std::declval<__type87>(), std::declval<__type130>()))) __type144;
    typedef decltype((pythonic::operator_::div(std::declval<__type143>(), std::declval<__type144>()))) __type145;
    typedef container<typename std::remove_reference<__type145>::type> __type146;
    typedef typename __combined<__type125,__type146>::type __type147;
    typedef typename __combined<__type147,__type27>::type __type148;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type133>(), std::declval<__type101>())) __type149;
    typedef decltype(std::declval<__type33>()[std::declval<__type149>()]) __type150;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type137>(), std::declval<__type105>())) __type151;
    typedef decltype(std::declval<__type37>()[std::declval<__type151>()]) __type152;
    typedef decltype((pythonic::operator_::mul(std::declval<__type150>(), std::declval<__type152>()))) __type153;
    typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type153>()))) __type154;
    typedef typename __combined<__type32,__type154>::type __type155;
    typedef typename __combined<__type155,__type153>::type __type156;
    typedef decltype((pythonic::operator_::mul(std::declval<__type120>(), std::declval<__type130>()))) __type157;
    typedef decltype((pythonic::operator_::div(std::declval<__type156>(), std::declval<__type157>()))) __type158;
    typedef container<typename std::remove_reference<__type158>::type> __type159;
    typedef typename __combined<__type148,__type159>::type __type160;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type>::type xix;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type131>::type::iterator>::value_type>::type>::type iy___;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type>::type xix__;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type48>::type::iterator>::value_type>::type>::type iy;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type48>::type::iterator>::value_type>::type>::type iy_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type>::type xix___;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type99>::type::iterator>::value_type>::type>::type ix_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type60>::type::iterator>::value_type>::type>::type ix;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type>::type xiy_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type99>::type::iterator>::value_type>::type>::type ix___;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type>::type xiy;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type>::type xix_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type60>::type::iterator>::value_type>::type>::type ix__;
    typename pythonic::lazy<__type8>::type ny;
    typename pythonic::lazy<__type8>::type nx;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type131>::type::iterator>::value_type>::type>::type iy__;
    ;
    ny= nx = (pythonic::operator_::add((pythonic::operator_::mul(pythonic::__builtin__::functor::int_{}(disp_max), 2L)), 1L));
    typename pythonic::assignable<decltype(std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im0)))>::type ny0 = std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im0));
    typename pythonic::assignable<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im0)))>::type nx0 = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im0));
    typename pythonic::assignable<decltype(std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im1)))>::type ny1 = std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im1));
    typename pythonic::assignable<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im1)))>::type nx1 = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, im1));
    ;
    typename pythonic::assignable<typename __combined<__type160,__type30>::type>::type correl = pythonic::numpy::functor::empty{}(pythonic::__builtin__::pythran::functor::make_shape{}(ny, nx), pythonic::numpy::functor::float32{});
    {
      for (long  xiy=0L; xiy < (pythonic::operator_::add(disp_max, 1L)); xiy += 1L)
      {
        typename pythonic::assignable<decltype((pythonic::operator_::add((-disp_max), xiy)))>::type dispy = (pythonic::operator_::add((-disp_max), xiy));
        typename pythonic::assignable<decltype((pythonic::operator_::add(ny1, pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy)), 0L))))>::type nymax = (pythonic::operator_::add(ny1, pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy)), 0L)));
        typename pythonic::assignable<decltype((-pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy)), 0L)))>::type ny1dep = (-pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy)), 0L));
        typename pythonic::assignable<decltype(pythonic::__builtin__::functor::max{}(0L, (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy))))>::type ny0dep = pythonic::__builtin__::functor::max{}(0L, (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy)));
        {
          for (long  xix=0L; xix < (pythonic::operator_::add(disp_max, 1L)); xix += 1L)
          {
            typename pythonic::assignable<decltype((pythonic::operator_::add((-disp_max), xix)))>::type dispx = (pythonic::operator_::add((-disp_max), xix));
            ;
            typename pythonic::assignable<decltype((-pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx)), 0L)))>::type nx1dep = (-pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx)), 0L));
            typename pythonic::assignable<decltype(pythonic::__builtin__::functor::max{}(0L, (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx))))>::type nx0dep = pythonic::__builtin__::functor::max{}(0L, (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx)));
            typename pythonic::assignable<typename __combined<__type75,__type73>::type>::type tmp = 0.0;
            {
              for (long  iy=0L; iy < nymax; iy += 1L)
              {
                {
                  long  __target139726228725544 = (pythonic::operator_::add(nx1, pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx)), 0L)));
                  for (long  ix=0L; ix < __target139726228725544; ix += 1L)
                  {
                    tmp += (pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple((pythonic::operator_::add(iy, ny1dep)), (pythonic::operator_::add(ix, nx1dep)))), im0.fast(pythonic::types::make_tuple((pythonic::operator_::add(ny0dep, iy)), (pythonic::operator_::add(nx0dep, ix))))));
                  }
                }
              }
            }
            correl.fast(pythonic::types::make_tuple(xiy, xix)) = (pythonic::operator_::div(tmp, (pythonic::operator_::mul((pythonic::operator_::add(nx1, pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx)), 0L))), nymax))));
          }
        }
        {
          for (long  xix_=0L; xix_ < disp_max; xix_ += 1L)
          {
            typename pythonic::assignable<decltype((pythonic::operator_::add(xix_, 1L)))>::type dispx_ = (pythonic::operator_::add(xix_, 1L));
            ;
            ;
            typename pythonic::assignable<decltype((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx_)))>::type nx0dep_ = (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx_));
            typename pythonic::assignable<typename __combined<__type110,__type108>::type>::type tmp_ = 0.0;
            {
              for (long  iy_=0L; iy_ < nymax; iy_ += 1L)
              {
                {
                  long  __target139726227829312 = (nx1 - pythonic::__builtin__::functor::max{}(((pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::functor::floordiv{}(nx0, 2L)), (pythonic::operator_::functor::floordiv{}(nx1, 2L)))), dispx_)) - nx0), 0L));
                  for (long  ix_=0L; ix_ < __target139726227829312; ix_ += 1L)
                  {
                    tmp_ += (pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple((pythonic::operator_::add(iy_, ny1dep)), (pythonic::operator_::add(ix_, 0L)))), im0[pythonic::types::make_tuple((pythonic::operator_::add(ny0dep, iy_)), (pythonic::operator_::add(nx0dep_, ix_)))]));
                  }
                }
              }
            }
            correl[pythonic::types::make_tuple(xiy, (pythonic::operator_::add((pythonic::operator_::add(xix_, disp_max)), 1L)))] = (pythonic::operator_::div(tmp_, (pythonic::operator_::mul((nx1 - pythonic::__builtin__::functor::max{}(((pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::functor::floordiv{}(nx0, 2L)), (pythonic::operator_::functor::floordiv{}(nx1, 2L)))), dispx_)) - nx0), 0L)), nymax))));
          }
        }
      }
    }
    {
      for (long  xiy_=0L; xiy_ < disp_max; xiy_ += 1L)
      {
        typename pythonic::assignable<decltype((pythonic::operator_::add(xiy_, 1L)))>::type dispy_ = (pythonic::operator_::add(xiy_, 1L));
        typename pythonic::assignable<decltype((ny1 - pythonic::__builtin__::functor::max{}(((pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::functor::floordiv{}(ny0, 2L)), (pythonic::operator_::functor::floordiv{}(ny1, 2L)))), dispy_)) - ny0), 0L)))>::type nymax_ = (ny1 - pythonic::__builtin__::functor::max{}(((pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::functor::floordiv{}(ny0, 2L)), (pythonic::operator_::functor::floordiv{}(ny1, 2L)))), dispy_)) - ny0), 0L));
        ;
        typename pythonic::assignable<decltype((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy_)))>::type ny0dep_ = (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(ny0, 2L)) - (pythonic::operator_::functor::floordiv{}(ny1, 2L))), dispy_));
        {
          for (long  xix__=0L; xix__ < (pythonic::operator_::add(disp_max, 1L)); xix__ += 1L)
          {
            typename pythonic::assignable<decltype((pythonic::operator_::add((-disp_max), xix__)))>::type dispx__ = (pythonic::operator_::add((-disp_max), xix__));
            ;
            typename pythonic::assignable<decltype((-pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx__)), 0L)))>::type nx1dep__ = (-pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx__)), 0L));
            typename pythonic::assignable<decltype(pythonic::__builtin__::functor::max{}(0L, (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx__))))>::type nx0dep__ = pythonic::__builtin__::functor::max{}(0L, (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx__)));
            typename pythonic::assignable<typename __combined<__type142,__type140>::type>::type tmp__ = 0.0;
            {
              for (long  iy__=0L; iy__ < nymax_; iy__ += 1L)
              {
                {
                  long  __target139726227893272 = (pythonic::operator_::add(nx1, pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx__)), 0L)));
                  for (long  ix__=0L; ix__ < __target139726227893272; ix__ += 1L)
                  {
                    tmp__ += (pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple((pythonic::operator_::add(iy__, 0L)), (pythonic::operator_::add(ix__, nx1dep__)))), im0[pythonic::types::make_tuple((pythonic::operator_::add(ny0dep_, iy__)), (pythonic::operator_::add(nx0dep__, ix__)))]));
                  }
                }
              }
            }
            correl[pythonic::types::make_tuple((pythonic::operator_::add((pythonic::operator_::add(xiy_, disp_max)), 1L)), xix__)] = (pythonic::operator_::div(tmp__, (pythonic::operator_::mul((pythonic::operator_::add(nx1, pythonic::__builtin__::functor::min{}((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx__)), 0L))), nymax_))));
          }
        }
        {
          for (long  xix___=0L; xix___ < disp_max; xix___ += 1L)
          {
            typename pythonic::assignable<decltype((pythonic::operator_::add(xix___, 1L)))>::type dispx___ = (pythonic::operator_::add(xix___, 1L));
            ;
            ;
            typename pythonic::assignable<decltype((pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx___)))>::type nx0dep___ = (pythonic::operator_::add(((pythonic::operator_::functor::floordiv{}(nx0, 2L)) - (pythonic::operator_::functor::floordiv{}(nx1, 2L))), dispx___));
            typename pythonic::assignable<typename __combined<__type155,__type153>::type>::type tmp___ = 0.0;
            {
              for (long  iy___=0L; iy___ < nymax_; iy___ += 1L)
              {
                {
                  long  __target139726227951800 = (nx1 - pythonic::__builtin__::functor::max{}(((pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::functor::floordiv{}(nx0, 2L)), (pythonic::operator_::functor::floordiv{}(nx1, 2L)))), dispx___)) - nx0), 0L));
                  for (long  ix___=0L; ix___ < __target139726227951800; ix___ += 1L)
                  {
                    tmp___ += (pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple((pythonic::operator_::add(iy___, 0L)), (pythonic::operator_::add(ix___, 0L)))), im0[pythonic::types::make_tuple((pythonic::operator_::add(ny0dep_, iy___)), (pythonic::operator_::add(nx0dep___, ix___)))]));
                  }
                }
              }
            }
            correl[pythonic::types::make_tuple((pythonic::operator_::add((pythonic::operator_::add(xiy_, disp_max)), 1L)), (pythonic::operator_::add((pythonic::operator_::add(xix___, disp_max)), 1L)))] = (pythonic::operator_::div(tmp___, (pythonic::operator_::mul((nx1 - pythonic::__builtin__::functor::max{}(((pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::functor::floordiv{}(nx0, 2L)), (pythonic::operator_::functor::floordiv{}(nx1, 2L)))), dispx___)) - nx0), 0L)), nymax_))));
          }
        }
      }
    }
    ;
    return pythonic::types::make_tuple((pythonic::operator_::mul(correl, pythonic::__builtin__::getattr(pythonic::types::attr::SIZE{}, im1))), pythonic::numpy::functor::sqrt{}((pythonic::operator_::mul(pythonic::numpy::functor::sum{}(pythonic::numpy::functor::square{}(im1)), pythonic::numpy::functor::sum{}(pythonic::numpy::functor::square{}(im0))))));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, long>::result_type correl_pythran0(pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im0, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl_pythran::correl_pythran()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, long>::result_type correl_pythran1(pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im0, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl_pythran::correl_pythran()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, long>::result_type correl_pythran2(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im0, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl_pythran::correl_pythran()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, long>::result_type correl_pythran3(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im0, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl_pythran::correl_pythran()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_correl_pythran0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"im0","im1","disp_max", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_pythran0(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_correl_pythran1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"im0","im1","disp_max", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_pythran1(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_correl_pythran2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"im0","im1","disp_max", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_pythran2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_correl_pythran3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"im0","im1","disp_max", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_pythran3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_correl_pythran(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_correl_pythran0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_correl_pythran1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_correl_pythran2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_correl_pythran3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "correl_pythran", "\n    - correl_pythran(float32[:,:], float32[:,:], int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "correl_pythran",
    (PyCFunction)__pythran_wrapall_correl_pythran,
    METH_VARARGS | METH_KEYWORDS,
    "Correlations by hand using only numpy.\n\n    Supported prototypes:\n\n    - correl_pythran(float32[:,:], float32[:,:], int)\n\n    Parameters\n    ----------\n\n    im0, im1 : images\n      input images : 2D matrix\n\n    disp_max : int\n      displacement max.\n\n    Notes\n    -------\n\n    im1_shape inf to im0_shape\n\n    Returns\n    -------\n\n    the computing correlation (size of computed correlation = disp_max*2 + 1)\n\n"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "correl_pythran",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(correl_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(correl_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("correl_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.2",
                                      "2019-05-23 15:41:03.520935",
                                      "47265bb7f080bb7ca6dedc248c1fa25e1ade86ac4ae4751f25736ea80d7ee89f");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif