#!/bin/bash
# 定时任务设置脚本
# 功能：自动运行养生/SEO关键词挖掘器

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${SCRIPT_DIR}/venv/bin/python"
MAIN_SCRIPT="${SCRIPT_DIR}/health_hot_seo_hunter.py"
LOG_DIR="${SCRIPT_DIR}/logs"

# 创建日志目录
mkdir -p "${LOG_DIR}"

echo "=================================================="
echo "🍵 养生/SEO关键词挖掘器 - 定时任务设置"
echo "=================================================="
echo ""
echo "脚本目录: ${SCRIPT_DIR}"
echo "Python路径: ${PYTHON_BIN}"
echo "主程序: ${MAIN_SCRIPT}"
echo "日志目录: ${LOG_DIR}"
echo ""

# 检查虚拟环境是否存在
if [ ! -f "${PYTHON_BIN}" ]; then
    echo "❌ 错误: 虚拟环境不存在！"
    echo "请先运行: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 创建运行脚本
cat > "${SCRIPT_DIR}/run_hunter.sh" << 'EOF'
#!/bin/bash
# 自动运行脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# 激活虚拟环境并运行
source venv/bin/activate
python health_hot_seo_hunter.py

# 记录日志
LOG_FILE="logs/run_$(date +%Y%m%d_%H%M%S).log"
echo "运行时间: $(date)" > "${LOG_FILE}"
echo "状态: 已完成" >> "${LOG_FILE}"
EOF

chmod +x "${SCRIPT_DIR}/run_hunter.sh"

echo "✅ 已创建运行脚本: run_hunter.sh"
echo ""

# 询问用户想要设置什么频率的定时任务
echo "请选择定时任务频率："
echo "1) 每小时运行一次"
echo "2) 每6小时运行一次"
echo "3) 每12小时运行一次"
echo "4) 每天早上9点运行"
echo "5) 每天晚上9点运行"
echo "6) 手动设置 (自定义cron表达式)"
echo "7) 查看当前定时任务"
echo "8) 删除所有定时任务"
echo "9) 退出"
echo ""
read -p "请输入选项 (1-9): " choice

case $choice in
    1)
        CRON_EXPR="0 * * * *"
        DESC="每小时"
        ;;
    2)
        CRON_EXPR="0 */6 * * *"
        DESC="每6小时"
        ;;
    3)
        CRON_EXPR="0 */12 * * *"
        DESC="每12小时"
        ;;
    4)
        CRON_EXPR="0 9 * * *"
        DESC="每天早上9点"
        ;;
    5)
        CRON_EXPR="0 21 * * *"
        DESC="每天晚上9点"
        ;;
    6)
        echo ""
        echo "请输入自定义cron表达式 (例如: 0 9 * * * 表示每天9点)"
        echo "格式: 分 时 日 月 周"
        read -p "cron表达式: " CRON_EXPR
        DESC="自定义"
        ;;
    7)
        echo ""
        echo "当前的定时任务:"
        crontab -l 2>/dev/null | grep -F "run_hunter.sh" || echo "没有设置定时任务"
        exit 0
        ;;
    8)
        echo ""
        echo "正在删除所有定时任务..."
        crontab -l 2>/dev/null | grep -v -F "run_hunter.sh" | crontab -
        echo "✅ 已删除所有定时任务"
        exit 0
        ;;
    9)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

# 添加到crontab
TEMP_CRON=$(mktemp)
crontab -l 2>/dev/null | grep -v -F "run_hunter.sh" > "${TEMP_CRON}" || true
echo "${CRON_EXPR} cd ${SCRIPT_DIR} && ${SCRIPT_DIR}/run_hunter.sh >> ${LOG_DIR}/cron.log 2>&1" >> "${TEMP_CRON}"
crontab "${TEMP_CRON}"
rm "${TEMP_CRON}"

echo ""
echo "✅ 定时任务设置成功！"
echo ""
echo "运行频率: ${DESC}"
echo "Cron表达式: ${CRON_EXPR}"
echo ""
echo "定时任务日志: ${LOG_DIR}/cron.log"
echo ""
echo "手动运行命令:"
echo "  ${SCRIPT_DIR}/run_hunter.sh"
echo ""
echo "查看定时任务:"
echo "  crontab -l"
echo ""
echo "查看定时任务日志:"
echo "  tail -f ${LOG_DIR}/cron.log"
echo ""
