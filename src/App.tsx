/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { 
  Monitor, 
  MousePointer2, 
  Video, 
  Play, 
  Square, 
  Save, 
  Settings, 
  Terminal, 
  Download,
  ShieldAlert,
  Cpu,
  Zap,
  Layers,
  BookOpen,
  ChevronRight,
  CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

const SidebarItem = ({ icon: Icon, label, active, onClick }: { icon: any, label: string, active: boolean, onClick: () => void }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
      active 
        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
        : 'text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200'
    }`}
  >
    <Icon size={18} />
    <span className="font-medium text-sm">{label}</span>
  </button>
);

const Card = ({ children, title, icon: Icon }: { children: React.ReactNode, title: string, icon: any }) => (
  <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 backdrop-blur-sm">
    <div className="flex items-center gap-2 mb-6 text-zinc-100">
      <Icon size={20} className="text-emerald-400" />
      <h2 className="text-lg font-semibold">{title}</h2>
    </div>
    {children}
  </div>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('visual');

  return (
    <div className="min-h-screen bg-black text-zinc-300 font-sans selection:bg-emerald-500/30">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 bottom-0 w-64 bg-zinc-950 border-r border-zinc-800 p-4 flex flex-col gap-8">
        <div className="flex items-center gap-3 px-2">
          <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
            <Zap size={20} className="text-black fill-current" />
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">YaoMouse <span className="text-emerald-500">Toolbox</span></h1>
        </div>

        <nav className="flex flex-col gap-2">
          <SidebarItem 
            icon={Monitor} 
            label="视觉触发任务" 
            active={activeTab === 'visual'} 
            onClick={() => setActiveTab('visual')} 
          />
          <SidebarItem 
            icon={MousePointer2} 
            label="增强型点击器" 
            active={activeTab === 'clicker'} 
            onClick={() => setActiveTab('clicker')} 
          />
          <SidebarItem 
            icon={History} 
            label="全功能录制器" 
            active={activeTab === 'recorder'} 
            onClick={() => setActiveTab('recorder')} 
          />
          <SidebarItem 
            icon={BookOpen} 
            label="安装教学" 
            active={activeTab === 'tutorial'} 
            onClick={() => setActiveTab('tutorial')} 
          />
        </nav>

        <div className="mt-auto p-4 bg-zinc-900/50 rounded-xl border border-zinc-800">
          <div className="flex items-center gap-2 text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2">
            <ShieldAlert size={12} />
            系统状态
          </div>
          <div className="flex items-center gap-2 text-sm text-emerald-400">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            核心引擎已就绪
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="ml-64 p-8 max-w-6xl mx-auto">
        <header className="mb-12 flex justify-between items-end">
          <div>
            <h2 className="text-4xl font-bold text-white mb-2 tracking-tight">
              {activeTab === 'visual' && '视觉-动作套件'}
              {activeTab === 'clicker' && '极速点击模块'}
              {activeTab === 'recorder' && '高保真录制器'}
            </h2>
            <p className="text-zinc-500 max-w-lg">
              工业级自动化，具备微秒级精度和确定性执行能力。
            </p>
          </div>
          <div className="flex gap-3">
            <button className="flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white px-4 py-2 rounded-lg transition-colors border border-zinc-700">
              <Terminal size={16} />
              查看日志
            </button>
            <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg transition-colors shadow-lg shadow-emerald-900/20">
              <Download size={16} />
              导出脚本
            </button>
          </div>
        </header>

        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            {activeTab === 'visual' && (
              <>
                <Card title="任务配置" icon={Settings}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs font-bold text-zinc-500 uppercase mb-2">任务名称</label>
                      <input type="text" className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2 focus:outline-none focus:border-emerald-500/50 transition-colors" placeholder="例如：自动登录序列" />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <button className="flex flex-col items-center gap-3 p-4 bg-zinc-800/50 border border-zinc-700 rounded-xl hover:bg-zinc-800 transition-colors group">
                        <Monitor className="text-zinc-500 group-hover:text-emerald-400 transition-colors" />
                        <span className="text-sm font-medium">截取触发图</span>
                      </button>
                      <button className="flex flex-col items-center gap-3 p-4 bg-zinc-800/50 border border-zinc-700 rounded-xl hover:bg-zinc-800 transition-colors group">
                        <Play className="text-zinc-500 group-hover:text-emerald-400 transition-colors" />
                        <span className="text-sm font-medium">录制序列</span>
                      </button>
                    </div>
                    <button className="w-full bg-emerald-600/10 text-emerald-400 border border-emerald-500/20 py-3 rounded-xl font-bold hover:bg-emerald-600/20 transition-all">
                      保存视觉任务
                    </button>
                  </div>
                </Card>
                <Card title="活动存档" icon={Layers}>
                  <div className="space-y-2">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="flex items-center justify-between p-3 bg-zinc-950/50 border border-zinc-800 rounded-lg group">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-zinc-800 rounded-lg overflow-hidden border border-zinc-700">
                            <img src={`https://picsum.photos/seed/task${i}/40/40`} alt="Trigger" referrerPolicy="no-referrer" />
                          </div>
                          <div>
                            <div className="text-sm font-medium text-zinc-200">任务_00{i}_触发器</div>
                            <div className="text-xs text-zinc-500">阈值: 0.95 | 12 个动作</div>
                          </div>
                        </div>
                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button className="p-2 hover:bg-zinc-800 rounded-lg text-zinc-400 hover:text-white"><Play size={14} /></button>
                          <button className="p-2 hover:bg-zinc-800 rounded-lg text-zinc-400 hover:text-red-400"><Square size={14} /></button>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </>
            )}

            {activeTab === 'clicker' && (
              <>
                <Card title="点击参数" icon={Cpu}>
                  <div className="space-y-6">
                    <div>
                      <label className="block text-xs font-bold text-zinc-500 uppercase mb-2">点击频率 (毫秒)</label>
                      <input type="number" className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2 focus:outline-none focus:border-emerald-500/50" defaultValue={100} />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-zinc-500 uppercase mb-2">按键选择</label>
                      <div className="grid grid-cols-2 gap-2">
                        <button className="py-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg font-medium">左键点击</button>
                        <button className="py-2 bg-zinc-800 border border-zinc-700 text-zinc-400 rounded-lg font-medium">右键点击</button>
                      </div>
                    </div>
                    <button className="w-full bg-emerald-600 text-white py-4 rounded-xl font-bold text-lg shadow-lg shadow-emerald-900/20 hover:bg-emerald-500 transition-all">
                      启动点击器
                    </button>
                  </div>
                </Card>
                <Card title="性能监控" icon={Zap}>
                  <div className="h-48 flex items-center justify-center border border-zinc-800 rounded-xl bg-zinc-950/50">
                    <div className="text-center">
                      <div className="text-4xl font-mono font-bold text-emerald-500">0.00</div>
                      <div className="text-xs text-zinc-500 uppercase tracking-widest mt-2">每秒点击次数 (CPS)</div>
                    </div>
                  </div>
                </Card>
              </>
            )}

            {activeTab === 'recorder' && (
              <>
                <Card title="宏引擎" icon={Video}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs font-bold text-zinc-500 uppercase mb-2">宏名称</label>
                      <input type="text" className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2 focus:outline-none focus:border-emerald-500/50" placeholder="例如：日常任务路径-A" />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-xs font-bold text-zinc-500 uppercase mb-2">循环次数</label>
                        <input type="number" className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2 focus:outline-none focus:border-emerald-500/50" defaultValue={1} />
                      </div>
                      <div className="flex items-end">
                        <label className="flex items-center gap-2 text-sm cursor-pointer">
                          <input type="checkbox" className="w-4 h-4 rounded border-zinc-800 bg-zinc-950 text-emerald-500 focus:ring-emerald-500/20" />
                          无限循环
                        </label>
                      </div>
                    </div>
                    <div className="pt-4 flex gap-3">
                      <button className="flex-1 bg-red-500/10 text-red-500 border border-red-500/20 py-3 rounded-xl font-bold hover:bg-red-500/20 transition-all">
                        录制路径
                      </button>
                      <button className="flex-1 bg-zinc-800 text-white py-3 rounded-xl font-bold hover:bg-zinc-700 transition-all">
                        加载宏
                      </button>
                    </div>
                  </div>
                </Card>
                <Card title="最近路径" icon={Save}>
                  <div className="space-y-2">
                    {['每日副本运行', '背包自动整理', '市场行情监控'].map(name => (
                      <div key={name} className="flex items-center justify-between p-3 bg-zinc-950/50 border border-zinc-800 rounded-lg">
                        <span className="text-sm font-medium text-zinc-300">{name}.macro</span>
                        <div className="flex gap-2">
                          <button className="text-xs text-emerald-400 hover:underline">加载</button>
                          <button className="text-xs text-red-400 hover:underline">删除</button>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </>
            )}

            {activeTab === 'tutorial' && (
              <div className="col-span-full space-y-6">
                <Card title="Windows 10 环境部署与运行教学" icon={BookOpen}>
                  <div className="space-y-8">
                    <div className="flex gap-4">
                      <div className="flex-shrink-0 w-8 h-8 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center font-bold">1</div>
                      <div className="space-y-2">
                        <h3 className="text-white font-bold">安装 Python 运行环境</h3>
                        <p className="text-sm text-zinc-400">前往 <a href="https://www.python.org/downloads/" target="_blank" className="text-emerald-400 underline">Python 官网</a> 下载最新版 (推荐 3.10 或更高)。</p>
                        <div className="bg-red-500/10 border border-red-500/20 p-3 rounded-lg flex items-start gap-2">
                          <ShieldAlert size={16} className="text-red-500 mt-0.5" />
                          <p className="text-xs text-red-400 font-medium">重要：安装时务必勾选 "Add Python to PATH" 选项！否则无法在命令行运行。</p>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-4">
                      <div className="flex-shrink-0 w-8 h-8 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center font-bold">2</div>
                      <div className="space-y-2">
                        <h3 className="text-white font-bold">解压代码压缩包</h3>
                        <p className="text-sm text-zinc-400">将从 GitHub 下载的 ZIP 文件右键解压到任意文件夹（例如桌面）。</p>
                      </div>
                    </div>

                    <div className="flex gap-4">
                      <div className="flex-shrink-0 w-8 h-8 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center font-bold">3</div>
                      <div className="space-y-2">
                        <h3 className="text-white font-bold">安装依赖库</h3>
                        <p className="text-sm text-zinc-400">在解压后的文件夹空白处，按住 <kbd className="bg-zinc-800 px-1 rounded">Shift</kbd> 并右键，选择“在此处打开 PowerShell 窗口”或“命令提示符”。</p>
                        <p className="text-sm text-zinc-400">输入以下命令并回车：</p>
                        <div className="bg-zinc-950 p-3 rounded-lg border border-zinc-800 font-mono text-xs text-emerald-400 flex justify-between items-center">
                          <code>pip install -r requirements.txt</code>
                          <button className="text-zinc-500 hover:text-white"><Download size={14} /></button>
                        </div>
                        <p className="text-xs text-zinc-500 italic">注：如果提示 pip 不是内部命令，说明步骤 1 的 PATH 没勾选，请重新安装 Python。</p>
                      </div>
                    </div>

                    <div className="flex gap-4">
                      <div className="flex-shrink-0 w-8 h-8 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center font-bold">4</div>
                      <div className="space-y-2">
                        <h3 className="text-white font-bold">启动程序</h3>
                        <p className="text-sm text-zinc-400">在同一个窗口中输入以下命令启动：</p>
                        <div className="bg-zinc-950 p-3 rounded-lg border border-zinc-800 font-mono text-xs text-emerald-400">
                          <code>python vibecontrol_pro.py</code>
                        </div>
                      </div>
                    </div>

                    <div className="pt-6 border-t border-zinc-800">
                      <div className="flex items-center gap-2 text-emerald-400 mb-4">
                        <Zap size={18} />
                        <h3 className="font-bold">进阶：生成独立 EXE 可执行文件</h3>
                      </div>
                      <div className="space-y-4">
                        <p className="text-sm text-zinc-400">如果你想把程序打包成一个双击即可运行的 .exe 文件（不需要再输入命令），请按照以下步骤操作：</p>
                        <div className="space-y-3">
                          <div className="flex items-start gap-2">
                            <ChevronRight size={14} className="text-emerald-500 mt-1" />
                            <p className="text-sm text-zinc-400">1. 安装打包工具：在命令行输入 <code className="text-emerald-400 bg-zinc-950 px-1 rounded">pip install pyinstaller</code></p>
                          </div>
                          <div className="flex items-start gap-2">
                            <ChevronRight size={14} className="text-emerald-500 mt-1" />
                            <p className="text-sm text-zinc-400">2. 执行打包命令：</p>
                          </div>
                          <div className="bg-zinc-950 p-3 rounded-lg border border-zinc-800 font-mono text-xs text-emerald-400 ml-6">
                            <code>pyinstaller --noconsole --onefile vibecontrol_pro.py</code>
                          </div>
                          <div className="flex items-start gap-2">
                            <ChevronRight size={14} className="text-emerald-500 mt-1" />
                            <p className="text-sm text-zinc-400">3. 获取文件：等待几分钟后，在文件夹里会出现一个 <code className="text-zinc-200 font-bold">dist</code> 文件夹，里面就是生成的 <code className="text-emerald-400 font-bold">vibecontrol_pro.exe</code>。</p>
                          </div>
                        </div>
                        <div className="bg-zinc-800/50 p-3 rounded-lg border border-zinc-700">
                          <p className="text-xs text-zinc-500 italic">注意：打包后的 EXE 可能会被杀毒软件误报，请添加信任或关闭杀毒软件运行。</p>
                        </div>
                      </div>
                    </div>

                    <div className="pt-6 border-t border-zinc-800">
                      <div className="flex items-center gap-2 text-emerald-400 mb-4">
                        <CheckCircle2 size={18} />
                        <h3 className="font-bold">常见问题排查</h3>
                      </div>
                      <ul className="list-disc list-inside text-sm text-zinc-500 space-y-2">
                        <li>提示 <code className="text-zinc-300">ModuleNotFoundError</code>: 说明依赖没装全，请重新执行步骤 3。</li>
                        <li>程序启动后没反应: 检查是否有杀毒软件拦截了模拟点击操作。</li>
                        <li>紧急停止: 运行中如需停止，请按键盘左上角的 <kbd className="bg-zinc-800 px-1 rounded">ESC</kbd> 键。</li>
                      </ul>
                    </div>
                  </div>
                </Card>
              </div>
            )}
          </motion.div>
        </AnimatePresence>

        <footer className="mt-12 p-6 bg-zinc-900/30 border border-zinc-800 rounded-2xl">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-zinc-800 rounded-xl">
              <ShieldAlert className="text-zinc-400" size={24} />
            </div>
            <div>
              <h4 className="text-white font-semibold">需要本地执行</h4>
              <p className="text-sm text-zinc-500">
                由于浏览器安全沙箱限制，自动化引擎必须在本地执行。
                请运行 <code className="text-emerald-400 bg-emerald-500/5 px-1 rounded">YaoMouse Toolbox</code> 脚本开始使用。
              </p>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
