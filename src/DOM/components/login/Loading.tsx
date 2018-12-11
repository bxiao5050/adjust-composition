import './Loading.scss'
import * as React from 'react'
import Login from 'Src/DOM/components/login'
import App from 'Src/DOM/App';
import Utils from 'Src/Base/Utils';

type LoadingProp = {
  Login: Login
  App: App
}

export default class Loading extends React.Component<LoadingProp, {}, any>  {

  constructor(props: LoadingProp) {
    super(props)
  }

  state = {
    clock: null
  }

  componentDidMount() {
    this.setState({
      clock: setTimeout(() => {
        var { userType, accountType } = SDK.GetUser()
        var isGuest = Utils.getAccountType(userType, accountType) === 'guest' ? true : false;
        App.instance.hideLogin()
        App.instance.showHover(isGuest)
        window.rgAsyncInit && window.rgAsyncInit()
      }, 2000)
    })
  }

  unclock = () => {
    clearTimeout(this.state.clock)
  }

  componentWillUnmount() {
    this.unclock()
  }

  render() {

    var user: UserInfo = SDK.GetUser()
    var password: string = user.password

    return <div className="content win-loading">
      <h2 className="logo block">IPOCKET GAMES</h2>
      <div className="info">
        <p>{SDK.config.i18n.txt_account_name}:  <span>{user.userName}</span></p>
        <p>{SDK.config.i18n.dom007}: <span>{(password ? password.substring(0, 10) : "") + '...'}</span></p>
      </div>
      <div className="loading">{SDK.config.i18n.dom005}</div>
      <div className="line"></div>
      <a className="change" onClick={() => {
        this.unclock();
        this.props.Login.props.history.goBack()
      }}>
        <span className="switch"></span>
        <span>{SDK.config.i18n.dom003}</span>
      </a>
    </div>
  }

}